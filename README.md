# Petal Homework

## What's the app look like

I reached for Flask! I have no experience with Flask ha, but it was a solid learning opportunity I couldn't pass up. The app defines a few HTTP endpoints (GET and POST on `/v1`) and defers business logic to `upreverse.py`. There is a `test_upreverse.py` file that tests both reversing and upcasing a string. Tests use `pytest` with a `requests_mock` module to prevent turning these unit tests into integration tests. Local development is made easier using Docker and docker-compose; the app can be built and packaged into an image using a Dockerfile, while bind-mounting the code onto the container with docker-compose allows for some hot reload capabilities.

In terms of what the app does, it'll take a JSON payload, `{"data": "reverse me"}`, POSTed to the `/v1` endpoint and returns a JSON payload, `{"data": "EM ESREVER"}`, with the contents of `data` upcased and reversed.

## What's the pipeline look like?

I opted to take this opportunity to kinda go ham. I leaned into a lot of tech that I have theoretical knowledge about, but nothin' practical. For the purposes of this exercise I'm using CircleCI as my CI/CD platform (feel free to check out [.circleci/config.yml](https://github.com/Bearlock/petal-homework/blob/main/.circleci/config.yml) for more). When a PR is merged against the `main` branch, CircleCI kicks in and will do two things:

1. It runs some really basic python tests. If those succeed,
2. It builds a new docker image and pushes it up to an AWS ECR image repo based off the Dockerfile.

It took a little bit for me to get the CircleCI incantations just right, but now it's completely out of my way. Everything builds like I would expect it to and I don't have to give it a second thought. The other sticky point for me was figuring out AWS' IAM rules for ECR, but again, once it works, it works.

So far so good!

## Gettin' weird

So once you've got a good image build and it's living in a repo, what are you supposed to do with it? I decided to get outta my comfort zone and started messing around with [Flux](https://fluxcd.io/) and a locally hosted K8s instance via Minikube. Go full GitOps y'know? [Bearlock/petal-homework-config](https://github.com/Bearlock/petal-homework-config) is the state/config repository for my kubernetes cluster. Two interesting components that I've defined therein are a GitRepository and a HelmRelease. Essentially, on some defined interval, Flux will sync the `/charts` directory from the GitRepository([Bearlock/petal-homework](https://github.com/Bearlock/petal-homework) in this case). And then, on some other interval, the HelmRelease will kick in and `helm install` the aforementioned charts to my k8s cluster. The charts for petal-homework are pretty vanilla and [defined here](https://github.com/Bearlock/petal-homework/tree/main/charts/petal-homework).

Honestly, it was mindblowing to make a code or config change, watch it get through the pipeline, build a good image and stash it somewhere, and then have that image/config synced up to my kubernetes cluster automagically.

## How to make it better

I wanna emphasize that this is a really barebones deployment pipeline. There are a bunch of improvments that can be made, such as:

- All the observability — Right now this thing is a black box. Liveness and readiness probes are a must for the container so that a "good" state can be defined. Not to mention there is no handling of application logging or tracing. I'd pretty much want to implement the "high observability principle" outlined by [Redhat](https://www.redhat.com/en/resources/cloud-native-container-design-whitepaper)
- Security — I have no experience with what good security looks like in a k8s cluster and I'm sure I'm doing something wrong.
- Better networking — I would love to have loadbalancers + nginx in front of the app container. Not to mention leveraging a real uWSGI/ASGI server — right now the application just uses whatever is built into flask :grimacing:
- Production ready python — The application needs to be a pluggable/installable component. Which means setting up a `setup.py` and turning the app into a package. Right now it uh, it isn't that.
- Production ready containers - The app doesn't autoscale or handle increasing load, it doesn't have good ways to recover itself, etc.
- Additional checks — More validation is always lovely. At the very least I'd appreciate a linting step in the build pipeline.
- Stratified deploys, multiple environments, etc — Right now the pipeline acts the same way for every branch. I'd prefer the pipeline to maybe build/deploy the application to a stage environment, and once that's been validated, promote the build to production or something. Or at the very least have a bulletproof canary/rolling deploy setup.
- Lack of practical experience — I think most of the tech I mentioned above is either new to me, or stuff I haven't used in a production/work environment; Flux, Flask, Helm, CircleCI, ECR are shiny new to me. Because of that, I am not aware of any gotchas, pitfalls, security issues, or best practices.
