# Port Self Service Webhooks with Ngrok

A Proof of Concept on how to quickly bootstrap a [getport.io](https://app.getport.io/) Self Service Actions with [ngrok](https://ngrok.com/) and [FastAPI](https://fastapi.tiangolo.com/)

## Why

### Background

* [Platform Engineering Dies in 4 Weeks](https://thenewstack.io/platform-engineering-dies-in-4-weeks/)
* [On platform adoption: essential mindsets and approaches](https://www.engineeringprimer.com/p/on-platform-adoption-essential-mindsets)

### The Core of the Problem 

![image](docs/images/why.png)

## High Level Architecture

![image](docs/architecture/high-level.png)

## Architecture Summary

* Port Self Service Actions are configured to POST to an [Ngrok Static Domain](https://ngrok.com/blog-post/free-static-domains-ngrok-users)
* FastAPI [Lifespan Events](https://fastapi.tiangolo.com/advanced/events/) create and destory a tunnel which is linked to an Ngrok Static Domain
* When FastAPI recieves a POST on the root path / it invokes a simulator run 
* If FastAPI recieves a POST on the /manual path. It will acknowledge the Webhook but not invoke a simulator. This so you can run  a simulator manually. 
* The simulator uses a semi structured module [port_api_runs]() containing both Pydantic Models and Native Python functions

## Lessons Learnt - So you don't have to

* Set Content-Type on headers to "application/json". I believe requests can do this automagically but didn't dig too deeply into it. 
* The link attribute in the [OpenAPI spec](https://api.getport.io/static/index.html#/Action%20Runs/patch_v1_actions_runs__run_id_) is defined as a string however it can be an array and you can have multiple links
* There is a [externalRunId](https://api.getport.io/static/index.html#/Action%20Runs/patch_v1_actions_runs__run_id_) attribute you can pass. I have modelled this but I am not sure what it does. I suspect it's something to do with Entities. 
* Ngrok allows one agent on the free tier. Not tearing down the agent and tunnel can lead to issues on subsequent run. 
* You can generate the JWT in the Port UI... however this is a short lived token. It's better to get a token at run time. 

## Architecture Decision Records (ADR)

* TODO

## Install and Run

> :warning:  ngrok, Pydantic and FastAPI libraries used in this MVP are sensitive to versions. Use of Virutal Environments is highly recommended 

* Obtain Ngrok Auth Token and Edge ID and set in [main.py]()
* Obtain a Port Client Secret and Client ID and set in [port_api_core.py]()

```bash
pip install -r requirements.txt
python main.py
```

A successful run should print the following in the terminal

![image](docs/images/terminal.png)

## Detailed Guides

* TODO

## Goals 

* Setup using minimal steps and code
  * This includes network infrastructure
  * Setup of a Port Self Service Action (i.e. no JQ with Body Params - just use the header (default))
* Naive Simulator to demo how to work with a Port Self Service Action
* Semi Realistic Simulated Scenarios (todo)
* Minimal Pydantic modeling
* Short lived experimentation - i don't refresh the JWT token or have logic to do this in this demo app. 

## Non Goals

* Full test suite
* Full Pydantic models for Port APIs (might be another project?)

## Why no Issues? 

* I have not enabled issues on this Github Repo
* As this is a Proof of Concept (PoC) repository, I do not intend to support it
* I would like to make sure that I don't mislead or frustrate those trying to use the code in this repo
* PRs are always welcomed 

## Todo 

* [ ] Turn [port_api_core]() in to a proper class
* [ ] [Webhook validation](https://docs.getport.io/create-self-service-experiences/setup-backend/webhook/signature-verification/) logic (core module) 
* [ ] Demonstrate MVP of Retrieving Blueprint and Action Run via API (i.e. minimal webhook config and use APIs to retrieve Self Service Action Details)
* [ ] Demonstrate [Tying Entities to an action run](https://docs.getport.io/create-self-service-experiences/reflect-action-progress/#tying-entities-to-an-action-run)
* [ ] More realistic example -> Temporary IP Whitelisting
* [ ] More realistic example -> Anonymized Prod database 
* [ ] Use Pydantic Settings with a .env file at root