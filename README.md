# Interest-seeker-Service

## Step 0. Motivation
Through my experience from teaching, I have discovered that student' are just forced to study and work.
As an educator, who is passionate about empowering students who are feeling lost and left in their journey
I was motivated to develop a chat-bot service that students can learn about themselves, seek their interest,
get recommeded some relevant works. In my ambition, I want students to be able to track their achivement and etc.
I believe in the power of the student. I know that they have so many potential that they can grow out and cheirsh their own 
ability.

## Step 1. Tools and its object
### 0. Chat-bot service
- Interest Matching : belive in platiscity : it will change, regular test and update
[Key Word: Plasticity in child development, Exposure to Diverse Activities, Providing Resources, Creating a Stimulating Environment
,Allowing Free Play, Encouraging Curiosity]
- Theraphy function, self-understanding + empowering
[Key Word: Confidence,Proper encouragement and Support]

### 1. Dash-board
- Interacting self tracker
: to be able to understand itself and to track itself in a better enviornment
- Recommendation System

==>Trobule: how to measure the interest
initial step: first let the user to select the top 3 interest, match it with vocation

second: make the questionaries based on ml, ai

### 2. Community
- exchanging interest and impression + material

## Step 2. Functionality
### 0. Chat-bot service
Q. How to identify one's interest
A. Data base + ML (maybe by some regression models):
    data base: https://www.onetcenter.org/database.html
    https://www.kaggle.com/datasets/lucasgreenwell/holland-code-riasec-test-responses 

Q. How to link one's interested area to a practical exposure
A. 1. Categorical search + classification
   2. Feedback system -> take some score and put it into a rec sys
    2-1. To build a rec sys
        - cold start: first until 100 user and 50 feedback
        <gradual exposure on the material>
        -> expose 5 youtube video, according to a category / keyword = youtube might be too vast so lets figure this out in the future -> maybe just selecting some nums of vid might help
        -> expose 5 article, according to a category / keyword
        -> expose 5 material from school curriculum
            ==> might get tricky what is the standard of recommendation
            thinking of getting data about the ratio of choosing different area of interest based on the test result
        <questions after exposing the material>
        - check the duration time, how long they stayed in the material reading , watching
        - asking content related question: check the rate of concentration
        - ask student directly : 
            1. how did you feel (positive/ not interested)
            : if positive
                2. are you willing to explore more relevant material
                3. which would you like
                 1) related experiments 2) interesting facts 3) work life (practical application) 4) recent research/ findings
            : if negative
                2. why you felt (content is boring / not interested in the theme)
                3. which would you like
                 1) rediscover my interest 2) show me random material, i will choose

## [Development Plan]
1. Chat bot dev
    1) Define how to measure interest
    2) How to rec / expect one's interest  
    = Use RIASEC model (Realistic, Investigative, Artistic, Social, Enterprising, Conventional)
    [ref:https://www.onetcenter.org/dl_files/Voc_Interests.pdf ]
    3) Chat bot development
    = after the test how to 'suggest' (recommned or predict)
        1) likely vocations that one will get [rel: https://www.onetcenter.org/reports/ML_OIPs.html]
        2) likely knoweldge that one will aspire to get
        => OBJECTIVE: Predicting a possible knowledge and skill that one will acquire


