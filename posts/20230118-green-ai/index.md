---
date: 2023-01-18T19:00:00
title: Green AI
type: ["posts"]
draft: false
tags:
categories:
---

One year ago I wrote a blog post about [machine learning and carbon emissions](https://erikjohannes.no/posts/20220105-machine-learning-and-carbon-emissions/). Since then, we have experienced some ground-breaking developments in the world of AI. With the release of image generators like DALL-E and large language models (LLMs) like ChatGPT, we are talking about a whole new scale of computational load for using, let alone training such models. What's more, these are no longer tools reserved for research purposes, but deployed software that people all over the world has started using on a daily basis.

In my research group, Trustworthy Green IoT Software at SINTEF Digital, we are exploring how we can contribute to Green AI, which refers to environmentally friendly AI development. One of the tools we have developed, an [ML pipeline for supervised learning](https://github.com/sintef-9012/erdre), uses [https://dvc.org](https://dvc.org/) for pipeline orchestration, which we see as a measure of reducing the energy usage through caching and skipping unnecessary reruns of pipeline stages. Many researchers are calling for measuring and reporting the carbon footprint in order to bring awareness to the issue, which is something we want to bring into our existing tools. The question is whether such measures are sufficient when the power of LLMs and similar tools is pushing the development in a much more resource-intensive direction.

If you are an AI/ML researcher or practitioner, how do you look at the increasing carbon footprint of ML models, and do you see "Green AI" as an important aspect for the future of AI development? Will the power of extremely large models always win over models with smaller footprint, or is it possible to find a balance between performance and energy efficiency?