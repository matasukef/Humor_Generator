test_data <- read.csv('../../../../media/matasuke/Ubuntu01/Projects/Humor_Generator/experiments/experiment1/static/data/test2.csv')

exp1 <- read.csv('~/../../../../media/matasuke/Ubuntu01/Projects/Humor_Generator/experiments/experiment1/static/result/exp1_result.csv')

pre_survey <- read.csv('~/../../../../media/matasuke/Ubuntu01/Projects/Humor_Generator/experiments/experiment1/static/result/pre_survey_result.csv')
SQH_score <- apply(pre_survey[4:7], MARGIN=1, sum)
MSHS_score <- apply(pre_survey[8:11], MARGIN=1, sum)

pre_survey_scores <- cbind(pre_survey[0:3], SQH_score, MSHS_score)

# bind scores with exp1
data <- merge(pre_survey_scores, exp1, by.x=c('age', 'name', 'sex'))

#merge result date with test_data
#merged_data = merge(data, test_data, by.x=c('image'))

EXP_NUM = 5
SIMS = c('origin', 'll', 'lh', 'hl', 'hh')

# calculate sum of all subjects for each sims
humor_scores = data.frame(data[1:5])
for(i in SIMS){
  label = paste('cap_', i, sep="")
  score = 0
  for(j in 1:EXP_NUM){
    name = paste('exp1_q', j, '_', i, sep="")
    score = score + data[name]
  }
  colnames(score) <- label
  humor_scores = data.frame(humor_scores, score)
  #transform(humor_scores, label=score)
}

# calculate each sims frequency
sims_frequenct = data.frame()
for(i in SIMS){
  label = paste('cap_', i, sep="")
  for(j in 1:EXP_NUM){
    name = paste('exp1_q', j, '_', i, sep="")
    print(data[name])
  }
}
