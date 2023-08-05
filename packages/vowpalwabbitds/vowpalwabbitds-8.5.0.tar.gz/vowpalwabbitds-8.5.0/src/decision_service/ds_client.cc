/*
Copyright (c) by respective owners including Yahoo!, Microsoft, and
individual contributors. All rights reserved.  Released under a BSD (revised)
license as described in the file LICENSE.
*/

#include "ds_api.h"
#include "ds_internal.h"
#include "ds_vw.h"
#include "event_hub_client.h"

#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/uuid/random_generator.hpp>
#include <boost/lockfree/queue.hpp>

#include <cpprest/http_client.h>

#include <memory>
#include <chrono>
#include <thread>

using namespace std::chrono_literals;

namespace Microsoft {
  namespace DecisionService {

    using namespace std;
    using namespace utility;
    using namespace web::http;
    using namespace web::http::client;
    using namespace concurrency;
    using namespace concurrency::streams;

    class DecisionServiceClientInternal {
    private:
      unique_ptr<VowpalWabbitThreadSafe> _pool;
      DecisionServiceConfiguration _config;

      boost::lockfree::queue<vector<unsigned char>*> _queue;

      std::vector<EventHubClient> _event_hub_interactions;
      EventHubClient _event_hub_observation;

      atomic_bool _thread_running;

      thread _upload_interaction_thread;
      thread _download_model_thread;

    public:
      DecisionServiceClientInternal(DecisionServiceConfiguration config)
        : _pool(new VowpalWabbitThreadSafe()),
        _config(config),
        _queue(config.batching_queue_max_size),
        _thread_running(true),
        // initialize n-clients
        _event_hub_interactions(config.num_parallel_connection, EventHubClient(config.eventhub_interaction_connection_string, config.certificate_validation_enabled)),
        _event_hub_observation(config.eventhub_observation_connection_string, config.certificate_validation_enabled),
        _upload_interaction_thread(&DecisionServiceClientInternal::upload_interactions, this),
        _download_model_thread(&DecisionServiceClientInternal::download_model, this)
      { }

      ~DecisionServiceClientInternal()
      {
        _thread_running = false;

        // wait for the threads to finish, don't delete before completion
        _upload_interaction_thread.join();
        _download_model_thread.join();

        // delete all elements from _queue
        vector<unsigned char>* item;
        while (_queue.pop(item))
          delete item;
      }

      void upload_reward(const char* event_id, const char* reward)
      {
        ostringstream payload;
        payload << "{\"EventId\":\"" << event_id << "\",\"v\":" << reward << "}";

        _event_hub_observation.Send(payload.str().c_str());
      }

      void enqueue_interaction(RankResponse& rankResponse)
      {
        std::ostringstream ostr;
        ostr << rankResponse;
        auto s = ostr.str();

        vector<unsigned char>* buffer = new vector<unsigned char>(s.begin(), s.end());
        _queue.push(buffer);
      }

    private:
      void download_model()
      {
        // TODO: download using cpprest
      }

      void upload_interactions()
      {
        vector<unsigned char>* json;
        vector<unsigned char>* json2;

        // populate initial already finished tasks
        vector<pplx::task<void>> open_requests;

        http_response initial_response;
        initial_response.set_status_code(201);

        for (auto& client : _event_hub_interactions)
        {
          pplx::task_completion_event<void> evt;
          evt.set();
          open_requests.push_back(pplx::task<void>(evt));
        }

        while (_thread_running)
        {
          if (!_queue.pop(json))
          {
            // empty
            // cout << "queue empty" << endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(_config.batching_timeout_in_milliseconds));

            continue;
          }

          int batch_count = 1;

          do
          {
            if (!_queue.pop(json2))
              json2 = nullptr;
            else
            {
              // check if we enough space
              if (json->size() + json2->size() < 256 * 1024 - 1)
              {
                // move get pointer to the beginning
                json->push_back('\n');
                json->insert(json->end(), json2->begin(), json2->end());

                batch_count++;

                // free memory
                delete json2;

                // accumulate more
                continue;
              }
            }

            // manage multiple outstanding requests...
            // send data
            auto ready_idx = pplx::when_any(open_requests.begin(), open_requests.end()).get();

            //printf("ready: %d length: %d batch count: %d status: %d\n",
            //  (int)ready_response.second, (int)json_str.length(), batch_count, ready_response.first.status_code());

            // send request and add back to task list
            open_requests[ready_idx] =
              _event_hub_interactions[ready_idx]
              .Send(json)
              .then([=](pplx::task<http_response> resp) {
              try
              {
                auto http_resp = resp.get();
                if (http_resp.status_code() != 201)
                  DS_LOG(_config, DecisionServiceLogLevel::error, "Failed to upload event: '" << http_resp.status_code() << "'")
              }
              catch (std::exception& e)
              {
                DS_LOG(_config, DecisionServiceLogLevel::error, "Failed to upload event: '" << e.what() << "'")
              }
            });

            // continue draining if we have another non-append json element
            json = json2;
            batch_count = 1;
          } while (json);
        }
      }

      friend class DecisionServiceClient;
    };


    DecisionServiceClient::DecisionServiceClient(DecisionServiceConfiguration& config)
      : _state(new DecisionServiceClientInternal(config))
    { }

    DecisionServiceClient::~DecisionServiceClient()
    { }

    RankResponse* DecisionServiceClient::rank_struct(const char* features, const char* event_id, const Array<int>& default_ranking)
    {
      return rank_cstyle(features, event_id, default_ranking.data, default_ranking.length);
    }

    RankResponse* DecisionServiceClient::rank_vector(const char* features, const char* event_id, const vector<int>& default_ranking)
    {
      return rank_cstyle(features, event_id, &default_ranking[0], default_ranking.size());
    }

    RankResponse* DecisionServiceClient::rank_cstyle(const char* features, const char* event_id, const int* default_ranking, size_t default_ranking_size)
    {
      /*
      cout << "features: '" << features << "'" << endl;
      for (size_t i = 0; i < default_ranking_size; i++)
        cout << "Default Rank " << i << ": " << default_ranking[i] << endl;
      */
      // generate event id if empty
      std::string l_event_id;
      if (!event_id || strlen(event_id) == 0)
        l_event_id = boost::uuids::to_string(boost::uuids::random_generator()());
      else
        l_event_id = event_id;

      // TODO: invoke VW
      // TODO: if no model provided use default ranking and impose epsilon-greedy exploration

      // invoke scoring to get a distribution over actions
      // std::vector<ActionProbability> ranking = _pool->rank(context);
      std::vector<int> ranking;
      ranking.push_back(1);
      ranking.push_back(0);

      std::vector<float> probs;
      probs.push_back(0.8f);
      probs.push_back(0.2f);

      RankResponse* response = new RankResponse(
        ranking,
        l_event_id.c_str(), "m1", probs, features);

      // invoke sampling
      // need to port random generator
      // need to port top slot explortation

      _state->enqueue_interaction(*response);

      return response;
    }

    void DecisionServiceClient::reward(const char* event_id, const char* reward)
    {
      _state->upload_reward(event_id, reward);
    }

    void DecisionServiceClient::update_model(unsigned char* model, size_t len)
    {
      update_model(model, 0, len);
    }

    void DecisionServiceClient::update_model(unsigned char* model, size_t offset, size_t len)
    {
      DS_LOG(_state->_config, DecisionServiceLogLevel::error, "update_model(len=" << len << ")")

      // TODO: swap out model
    }
  }
}
