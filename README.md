# Endre Márk Borza

This is a more casual, professional history page thing. No grand conclusion, just stuff listed mostly backward chronologically.

## CCL @ Corvinus

Started working in 2023 as a Research Data Engineer at [ccl](https://centerforcollectivelearning.org/), a multidisciplinary lab started in Budapest by an EU grant. I help others publish papers involving complex data pipelines, but mostly I worked on [rankless.org](https://www.rankless.org/) - a platform for the exploration of scholarly data. I managed to convince our director César - whose idea the site itself actually was - that I'd do the whole thing in Rust and Svelte without any large framework or ready-made tech like react, neo4j, or even anything SQL.

## Research

Since around 2014 I have been working on the data side of a bunch of papers and one [book](https://gabors-data-analysis.com/), first I got some "thanks" in the acknowledgments, then I started to get [credit as an author](https://scholar.google.com/citations?user=FzM5hAUAAAAJ&hl=en&oi=ao). There is a wide scope of topics here, from experimental economics, to park visitation patterns. The common thread is large, complex datasets that needed efficient processing, or creative analysis.

## Freelancing

Since I primarily work in academia since 2021, I did set up a gig where I can do consulting and development contract work still in the private sector. I find that it is nice to meet challenges that have market value and it's nice to get paid well. I had so far done some machine learning modeling and some highly convoluted data-collection. One of the drawbacks next to these great private sector benefits is that one can't really go into much detail.

## Research Big Data Team @ [KRTK](https://krtk.hun-ren.hu/en/homepage/)

In 2021 I set up a small team called [Social Science Computing Unit Budapest](https://sscu-budapest.github.io/) and we started to build a comprehensive data science toolset for scientific research. It slowed down a lot due to a range of issues, mostly around demand, but we did build a central dataset and data-project standard/framework named [datazimmer](https://github.com/sscu-budapest/datazimmer).
We also built tools around it like [colassigner](https://github.com/endremborza/colassigner) so that we don't use string literals with pandas so much, [parquetranger](https://github.com/endremborza/parquetranger) to manage - save, load, extend - large datasets in partitioned parquet files, a task queue orchestrator [atqo](https://github.com/endremborza/atqo), raw data collection manager [aswan](https://github.com/endremborza/aswan) - named after a dam, and some python package boilerplate [branthebuilder](https://github.com/endremborza/branthebuilder) so that we can start many others.

We also set up a _lot_ of datasets for research around retail, weather, job-listings, chess, real-estate, football, news articles, interconnected wiki-pages, movies, etc. many of them periodically, automatically updating. I'm still working on it as of 2025.

## Data Science @ Lidl

2018-2021 I worked at Lidl as a data scientist. It was interesting, challenging, paid well, I learned a lot. It was a demanding environment with high employee turnover but still high productivity. After a few years, I got tired of not being able to show anything I've done to anybody, and not owning any of the fruits of my labor, so I took a massive paycut and moved to academia.

We developed machine learning for demand prediction and algorithms to optimize delivery and distribution. We were quite successful, a lot of what we did got scaled up and is being used by Lidl widely. I also got to work with professional developers and infra people and gain experience with technologies less frequently used in data science jobs like Kubernetes, Kafka, Elasticsearch, a _lot_ of CI/CD and so on. I hope they don't sue me for exposing a few things they use. Yes, they were this protective of everything

## Teaching 

In 2015 I started teaching @ [Rajk](http://rajk.eu/home/), and since then have taught courses in Programming and Algorithm Design, Applied Algorithm Design for Data Processing, Statistical Methods for Causal Inference. I am also sometimes a guest instructor in machine learning and network science courses, both at rajk and at Corvinus.
Turns out, I quite like teaching, and Rajk, with small classes and generally motivated students, was a great fit. I even got awarded the Permanent Professors of Rajk College title, which might be my favorite thing I've got as an accolade and the one thing I will brag about without anyone asking.

## Lots of Building

I like building things for myself. It mostly helps me learn tools and concepts, but sometimes they turn out to be useful. 

**Libraries** to read/write [parquet](https://github.com/endremborza/shackleton) and [csv](https://github.com/endremborza/partcsv) in a parallel and efficient way in python. Entity coreference in both [python](https://github.com/endremborza/encoref) and [Julia](https://github.com/endremborza/Encoref.jl), 
a [Julia library](https://github.com/endremborza/BigO.jl) for complexity plotting and estimation.

**Apps** like [a browser extension](https://github.com/endremborza/scimagojr-search-engine) to search for a scientific journal with one right-click (and then a left-click), 
a small [dash app](https://github.com/endremborza/typegame) for creating quizzes for programming education,
docker-based [comparison tool](https://github.com/endremborza/fibonacci_language_comparison) of programming languages, running the same algorithm, with an interface for guessing results. Also a bunch of apps for [rajk](http://rajk.eu/home/) college, where I spent a wonderful 7 years and got to make tools for resolving preference-based [course applications](https://github.com/rajk-apps/riki), uploading coursework, [credit-card processing](https://github.com/rajk-apps/rajksimple), teaching aids for [presenting](https://github.com/endremborza/teach) or [evaluation](https://jkg-evaluators.readthedocs.io/en/latest/index.html), tinder-like quick evaluation tools for collective decision making and many failed others. I tried vanilla javascript with google sheets backends, raw PHP 5, and eventually Django. Most of them got the job done at the time, but for me the biggest benefit was getting my hands dirty, even before working together with a group of senior, experienced developers later.

These are mostly some sort of software that all become stale as versions move on. **Simple tools**, are fun because they can just be _done_, like an interactive [article](https://endremborza.github.io/funtum-computing/) explaining quantum states and gates with hand-rolled 3d SVGs of Bloch-spheres, or a [tool](https://endremborza.github.io/static-snippets/box) that helps my friend figure out how to cut a few pieces of wood to make a house-like bed for my godson.

## Contributions

I think open-source contributions are a great way to learn, and so a while I did a bit of that but lost a bit of interest recently. However, I managed to contribute to [pandas](https://github.com/pandas-dev/pandas/commits?author=endremborza), [dask](https://github.com/dask/dask/commits?author=endremborza), [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling/commits?author=endremborza), [julia](https://github.com/JuliaLang/julia/commits?author=endremborza), [fsspec](https://github.com/fsspec/filesystem_spec/commits?author=endremborza), [dvc](https://github.com/iterative/dvc/commits?author=endremborza).

What was really nice however, is [a project of mine](https://github.com/endremborza/sqlmermaid) that visualizes sql schemas with python even got a PR from a random person. I merged it, it was lovely, since I never really promote any of this.
