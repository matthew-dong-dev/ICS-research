
2/19/20

- Good job making your first design decision when figuring out how to implement instructor search w/ Max. by choosing to a parent component instead of hacking the data.  Can copy functions over bc we don't want premature optimization but we do want clean design.  

Reasons for a pay raise

1. search feature - top level nav feature
1. publication - first author
1. whole system familiarity - done work on FE, BE, Models, Data
1. currently sharing admin resposibilities on Data so jeff isn't single point of failure for everything
1. mentoring URAPs - instructor search

1/28/20

With greater context you're realizing yes this is a cool project and yes you're in a little over your head.  No way you should be in this role you're in where you're basically the admin of the data pipeline, good thing you took it seriously and taught yourself what you needed.  Working on askoski is really organic, you're doing a job a full time swe should be doing and you should embrace it and learn as much as you can.  
    - what is the size of the data being used - see the research paper
    - 100K students, 2M enrollment records since 2008, ~10k courses? 

If people ask what you do for the project - you do whatever work is necessary: FE, BE work, data pipeline, ml modeling, but no system architecture or devops (yet).

There's a tradeoff, prod keeps breaking now (e.g. data pipeline broke prod for entire F19 semester and you broke prod twice by removing files it was using and changing some RNN scripts) but that's bc we're developing up the pipelines and cleaning up tech debt to make sure we're forward compatible to things like multi campus and more stable moving forward (closer to CI/CD)

1/16/20

After 2 months you finally know what you don't know regarding the data pipeline and are able to begin to grok where the lookup table error occurred.

12/11/19

Now you're more or less settled into the data role - you're not familiar with the internal logic yet, but know how things work from high level overview. 

1. Get an overview of the repo & pipeline.  Where does everything live, what comes directly from campus registrar and what comes from the APIs?  
1. Then fill in knowledge gaps & reconcile all the moving parts to determine what the the next action item is.  
1. Things are pretty organic, Zach doesn't exactly know what's going around either and you have free reign for what direction you want to pursue.  
1. You're willing to be the main point person for this pipeline so you're trying to absorb as much information so you can start working on actions items, which will help you figure out what you don't know.  

11/1/19

- Finally moving from FE & ML --> BE & Data

GJ putting in 9.5 hours of playing around with the flask service and FE model to get comfortable with everything before you got a concrete task, it was distributed over 3 weeks when you were extremely busy but the fact that you made those small sacrifices significantly lowered the barrier to entry to allow you to contribute faster

- 9/22 - 9/29 = 1.25 + .5 +.5 +.5 +.5 + .5 = 3.75
- 9/30 - 10/6 = .5*7 = 3.5
- 10/7 - 10/10 = .5+.75 + .5 + .5 = 2.25
- Total = 9.5

Dev job training / SWE Immersion to also enable the transition:

- 10/19 - 10/20 = 1.5 + 1.5 + 1.5+1.5 + .75 = 6.75 

10/11/19

- you may not have been working on anything concrete for the past 3 weeks after putting together the ECTEL presentation but you've been getting familiar with the BE over this time in 30 minute spikes and that's accumulated into 10.5 hours of work that you don't have to do now that you finally have something to work on

10/10/19

- askoski is really a cutting edge project that you should stay onboard of and on top of in terms of contributions.  In hindsight you realize you should not be on this project, 36 people applied through URAP most of them were already more qualified than you were when you simply emailed Zach as a freshman.   

10/2/19:

- Still don't have any concrete task to work on
- Also getting familiar with all the moving parts of the FE models and BE service is a lot more than anticipated
- Now that your schedule is settled in, start setting deadlines for when you should have certain action items done, when you should touch base with people, or timebox certain tasks so don't get lost in the weeds

9/9/19: More concrete tasks once UCI approval goes through / Plan features does user study.  In the meanwhile: 

1. refamiliarize self with codebase in particular BE service
1. research parallelization of models-askoski training - the bottleneck is SGD in the course2vec model
    - this looks like it would require you to learn how to write a simple model in pytorch, how course2vec specifically works, how [parallelization across GPUs work](https://pytorch.org/tutorials/beginner/blitz/data_parallel_tutorial.html), before you can even think about figuring out how to apply it to your use case

8/27/19:

- discuss future work: not so interested in FE dev / Don't want to be wedded to the search feature, Would be more interested in working on data pipelines, flask service actions items, test coverage, data requirements for UCI deployment etc..
- more interested in working on backend tasks, course APIs - anything from to do or the parking lot?   help w/ the data unification between the features / AC courses
