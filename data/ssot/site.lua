local d = require("dsl")
local p, b, a, ul, h4, strong, em = d.p, d.b, d.a, d.ul, d.h4, d.strong, d.em

---@type Site
return {
  root = "home",
  nodes = {
    {
      id = "home",
      title = "I am",
      body = {
        p { b "Endre Borza", ". made this page to collect and structure the work I've done, and some things I like." },
        p({ "It is set up in this experimental layout, you can flatten it ", a("./flat", "here"), "." }, "fancy-layout"),
      },
      children = { "artifacts", "academia", "tools-tastes" },
    },
    {
      id = "artifacts",
      title = "Artifacts",
      body = {
        p "I built",
        ul {
          { a("https://www.rankless.org/", "Rankless"), ", an interactive platform for exploring massive scholarly datasets" },
          "Machine learning and optimization systems for retail logistics and football analytics",
          "Reusable tools and infrastructure that make my work easier",
        },
      },
      children = { "rankless", "data-at-scale", "applets" },
    },
    {
      id = "rankless",
      title = "Rankless",
      body = {
        p {
          "Originally conceived by Cesar Hidalgo at ",
          a("https://centerforcollectivelearning.org/", "CCL"),
          ", ",
          a("https://www.rankless.org/", "Rankless"),
          " was a great engineering challenge. It processes over 3 billion citations among 300 million papers and responds to complex interactive queries almost instantly.",
        },
        p "This required heavy optimization throughout: a specialized Rust backend with multi-stage compilation aligned to data shape and size, and a Svelte frontend with hand-rolled SVGs and practically no dependencies.",
      },
      children = { "ccl" },
    },
    {
      id = "data-at-scale",
      title = "Data at Scale",
      body = {
        h4 "Retail Data Science",
        p { b "2018", "-", b "2021", " I worked at Lidl as a data scientist. It was demanding, fast-paced, and productive. We built machine learning systems for demand prediction and optimization that were rolled out widely." },
        h4 "Freelance & Contract Work",
        p { "Since ", b "2021", " I occasionally take on consulting and development work in the private sector, or even some research projects. These are usually solutions to data engineering, data collection, machine learning or optimization problems." },
      },
      children = { "retail-ml", "football-ml", "research-infra" },
    },
    {
      id = "retail-ml",
      title = "Retail at Industrial Scale",
      body = {
        p { "Starting in ", b "2018", " at Lidl we developed machine learning models for demand forecasting and algorithms for delivery and distribution optimization." },
        p "The work scaled well and as far as I know is still in use. I also got deep exposure to production infrastructure: Kubernetes, Kafka, Elasticsearch, and a lot of CI/CD.",
        p "It was ruthless, difficult, and formative. In a small team, working mostly with developers, and trying to integrate the result of our work into the fine-tuned processes of the massive global behemoth that is Lidl.",
        p "I eventually left because I wanted more ownership of my work and the ability to show and reuse what I built.",
      },
    },
    {
      id = "football-ml",
      title = "Football Analytics",
      body = {
        p "Worked on ML models and iterative algorithm design for evaluating team performance, player value, and contract terms.",
        p "Some of this work fed into academic papers, sometimes using football as a parallel system to study incentives or behavior (e.g. referees).",
        p { "I also occasionally do small analyses for myself, like ", a("https://bits.borza.cc/pl-fixtures", "this one"), " on Premier League fixture difficulty." },
      },
      children = { "football-fun" },
    },
    {
      id = "applets",
      title = "Practical Software",
      body = {
        p "Tools I built to solve concrete problems. Some small, opinionated personal tools, reusable research infrastructure, and open-source work in established ecosystems.",
      },
      children = { "my-tools", "sscub-tools", "open-source" },
    },
    {
      id = "my-tools",
      title = "Personal Tools",
      body = {
        p "Small libraries and tools for parallel IO, dataset handling, entity resolution, to make repeated patterns explicit and reusable.",
        p {
          strong "Libraries",
          " to read/write ",
          a("https://github.com/endremborza/shackleton", "parquet"),
          " and ",
          a("https://github.com/endremborza/partcsv", "csv"),
          " in a parallel and efficient way in python. Entity coreference in both ",
          a("https://github.com/endremborza/encoref", "python"),
          " and ",
          a("https://github.com/endremborza/Encoref.jl", "Julia"),
          ", a ",
          a("https://github.com/endremborza/BigO.jl", "Julia library"),
          " for complexity plotting and estimation.",
        },
        p {
          strong "Apps",
          " like ",
          a("https://github.com/endremborza/scimagojr-search-engine", "a browser extension"),
          " to search for a scientific journal with one right-click (and then a left-click), a small ",
          a("https://github.com/endremborza/typegame", "dash app"),
          " for creating quizzes for programming education, docker-based comparison tool of programming languages, or implementations of students. Also a bunch of apps for ",
          a("https://rajk.eu", "Rajk"),
          " college, where I spent a wonderful 7 years and got to make tools for resolving preference-based ",
          a("https://github.com/rajk-apps/riki", "course applications"),
          ", uploading coursework, ",
          a("https://github.com/rajk-apps/rajksimple", "credit-card processing"),
          ", teaching aids for ",
          a("https://github.com/endremborza/teach", "presenting"),
          " or ",
          a("https://jkg-evaluators.readthedocs.io/en/latest/index.html", "evaluation"),
          ", tinder-like quick evaluation tools for collective decision making and many failed others. I tried vanilla javascript with google sheets backends, raw PHP 5, and eventually Django. Most of them got the job done at the time, but the biggest benefit was getting my hands dirty, even before working together with a group of senior developers later.",
        },
        p {
          "These are mostly some sort of software that all become stale as versions move on. ",
          strong "Simple tools",
          ", are fun because they can just be ",
          em "done",
          ", like an interactive ",
          a("https://endremborza.github.io/funtum-computing/", "article"),
          " explaining quantum states and gates with hand-rolled 3d SVGs of Bloch-spheres, or a ",
          a("https://endremborza.github.io/static-snippets/box", "tool"),
          " that helps my friend figure out how to cut a few pieces of wood to make a house-like bed for my godson.",
        },
      },
      children = { "work-environment" },
    },
    {
      id = "open-source",
      title = "Open Source",
      body = {
        p "I used to contribute more actively to open-source projects as a way to learn tools from the inside.",
        p {
          "Contributions include ",
          a("https://github.com/pandas-dev/pandas/commits?author=endremborza", "pandas"),
          ", ",
          a("https://github.com/dask/dask/commits?author=endremborza", "dask"),
          ", ",
          a("https://github.com/JuliaLang/julia/commits?author=endremborza", "Julia"),
          ", ",
          a("https://github.com/fsspec/filesystem_spec/commits?author=endremborza", "fsspec"),
          ", and ",
          a("https://github.com/iterative/dvc/commits?author=endremborza", "dvc"),
          ".",
        },
        p {
          a("https://github.com/endremborza/sqlmermaid", "A project of mine"),
          " that visualizes SQL schemas with python even got a random external PR once. I merged it. It felt great.",
        },
      },
    },
    {
      id = "sscub-tools",
      title = "Research Tooling",
      body = {
        p { "As part of SSCUB we built a shared data framework called ", a("https://github.com/sscu-budapest/datazimmer", "datazimmer"), "." },
        p {
          "We also built tools around it like ",
          a("https://github.com/endremborza/colassigner", "colassigner"),
          " so that we don't use string literals with pandas so much, ",
          a("https://github.com/endremborza/parquetranger", "parquetranger"),
          " to manage - save, load, extend - large datasets in partitioned parquet files, a task queue orchestrator ",
          a("https://github.com/endremborza/atqo", "atqo"),
          ", raw data collection manager ",
          a("https://github.com/endremborza/aswan", "aswan"),
          " - named after a dam, and some python package ",
          a("https://github.com/endremborza/branthebuilder", "boilerplate"),
          " so that we can start many others.",
        },
        p "These were designed for multi-project, multi-year research workflows.",
      },
      children = { "sscub" },
    },
    {
      id = "academia",
      title = "Research & Teaching",
      body = {
        p { "Since ", b "2014", " I've worked on the data side of some papers and one ", a("https://gabors-data-analysis.com/", "book"), ". Over time my role grew from acknowledgments to full authorship." },
        p "The topics vary widely, but the common thread is large, complex datasets that require efficient processing or creative analysis.",
        p { "In parallel, since ", b "2015", " I've been teaching programming, data-heavy methods, and some machine learning mostly in small, motivated settings." },
      },
      children = { "papers", "teaching", "research-infra" },
    },
    {
      id = "papers",
      title = "Papers",
      body = {
        p "I mostly contribute through data engineering, pipeline design, and scalable analysis.",
        p {
          "The work spans experimental economics, social science, and applied data analysis. ",
          a("https://scholar.google.com/citations?user=FzM5hAUAAAAJ&hl=en&oi=ao", "Google"),
          " collects the ones where I get author credit neatly.",
        },
      },
    },
    {
      id = "teaching",
      title = "Teaching",
      body = {
        p { "I started teaching in ", b "2015", " at ", a("https://rajk.eu", "Rajk College"), "." },
        p "Courses include programming, algorithm design, data processing, and causal inference. I also guest lecture in machine learning and network science. Sometimes at other institutions",
        p "I enjoy teaching a lot, especially in small classes with motivated students.",
      },
    },
    {
      id = "research-infra",
      title = "Research Infrastructure",
      body = {
        p "Much of my academic work is about building shared infrastructure that makes complex, data-heavy research possible.",
      },
      children = { "ccl", "sscub-tools", "sscub" },
    },
    {
      id = "ccl",
      title = "Center for Collective Learning",
      body = {
        p { "Since ", b "2023", " I've worked as a Research Data Engineer at ", a("https://centerforcollectivelearning.org/", "CCL"), "." },
        p { "I support research with complex data pipelines but mainly built ", a("https://www.rankless.org/", "Rankless"), "." },
        p "I also set up environments for large-scale computation.",
      },
      children = { "rankless" },
    },
    {
      id = "sscub",
      title = "Social Science Computing",
      body = {
        p {
          'In 2021 I was tasked with setting up some "Big Data Capabilities" at ',
          a("https://krtk.elte.hu/en", "the Centre for Economic and Regional Studies"),
          ", so I founded the ",
          a("https://sscu-budapest.github.io/", "Social Science Computing Unit"),
          " there.",
        },
        p "We built shared datasets, standards, and tooling for research across domains like retail, weather, football, news, chess, and real estate.",
        p "The Centre went through a lot of institutional and some personnel changes, and eventually demand for complex data intensive tasks fizzled out, and a lot of what did occur progressed slowly.",
      },
    },
    {
      id = "tools-tastes",
      title = "Tools & Tastes",
      body = {
        p "I use",
        ul {
          "Python, Rust, Svelte to build",
          "Neovim, Linux, LeftWM and a split keyboard for comfort",
          "AI mostly from the command line, selectively but appreciatively",
        },
        p "I'm interested in health and longevity and can spend a lot of time optimizing my knowledge management and living space. I also like to do at least one seriously physically challenging thing every year.",
      },
      children = { "work-environment", "play", "culture" },
    },
    {
      id = "work-environment",
      title = "Work Environment",
      body = {
        p "I prefer setups where everything is derived from code and reproducible.",
        p {
          "I keep my environment configuration ",
          a("https://github.com/endremborza/setup", "here"),
          ". It's not always perfectly up to date and comprehensive, but it reflects how I work. And it helps me create a complete working environment on a clean Ubuntu installation within 15 minutes",
        },
      },
    },
    {
      id = "play",
      title = "Games & Play",
      body = {
        p "I enjoy football (both kinds, but the European one a bit more), StarCraft, D&D and chess. I believe my tastes have developed independently of this, but I definitely enjoy that both chess and StarCraft have been primary playgrounds for AI advancements, both kinds of football have grown immense data science and engineering ecosystems and D&D was the basis for one of the most successful software development efforts I have seen in the XXI. century: Baldur's Gate 3.",
      },
      children = { "dnd", "football-fun" },
    },
    {
      id = "dnd",
      title = "D&D",
      body = {
        p { "I started playing in ", b "2020", ", and it turned out to be one of my primary recreational activities." },
        p {
          "I find that running a D&D campaign is the ultimate test of any incorporeal inventory and note-taking system. You need to build a world, quickly retrieve information, very quickly input new information, and keep track of the knowledge of the world from the point of view of several PCs and NPCs. After trying a great number of options from the PKM and note-taking space, I settled for the time on ",
          a("https://github.com/logseq/logseq", "Logseq"),
          ", but am constantly building and improving my setup.",
        },
      },
    },
    {
      id = "football-fun",
      title = "Football for Fun",
      body = {
        p "Played pretty seriously at youth level, fell in love with Manchester United at the best possible time - the semi-final of the 1999 Champions League",
        p "My love for football and determination to understand the wonderful complex mixture of signal and noise that is recorded of it in the form of more and more complex data actually contributed a lot to my professional path.",
      },
    },
    {
      id = "culture",
      title = "Reviews & Culture",
      body = {
        p {
          "I like writing short reviews from time to time about films, games, albums as it is great practice in expression. ",
          a("https://www.imdb.com/user/ur23979373/reviews", "Film reviews"),
          " are public on imdb, ",
          a("https://rateyourmusic.com/~endremborza", "music"),
          " is going a lot slower",
        },
      },
    },
  },
}
