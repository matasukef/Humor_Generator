exp1 <- read.csv('~/../../../../media/matasuke/Ubuntu01/Projects/Humor_Generator/experiments/experiment1/static/result/exp1_result.csv')

pre_survey <- read.csv('~/../../../../media/matasuke/Ubuntu01/Projects/Humor_Generator/experiments/experiment1/static/result/pre_survey_result.csv')
SQH_score <- apply(pre_survey[4:7], MARGIN=1, sum)
MSHS_score <- apply(pre_survey[8:11], MARGIN=1, sum)

pre_survey_scores <- cbind(pre_survey[0:3], SQH_score, MSHS_score)

# bind scores with exp1
data <- merge(pre_survey_scores, exp1, by.x=c('age', 'name', 'sex'))

#merge result date with test_data
#merged_data = merge(data, test_data, by.x=c('image'))

EXP_NUM = 50
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

cap_scores_sum = humor_scores[6:10]
cap_scores_mean = cap_scores_sum / EXP_NUM

#mean scores by col
each_cap_mean = apply(cap_scores_mean, MARGIN=2, mean)


# calculate each sims frequency to validate it is based on normal disctibution.
#sims_frequenct = data.frame()
#for(i in SIMS){
#  label = paste('cap_', i, sep="")
#  for(j in 1:EXP_NUM){
#    name = paste('exp1_q', j, '_', i, sep="")
#    print(data[name])
#  }
#}


# origin caps
origin_caps = data.frame(data[1:3])
for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_origin', sep="")
  origin_caps = data.frame(origin_caps, data[name])
}

# low low caps
ll_caps = data.frame(data[1:3])
for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_ll', sep="")
  ll_caps = data.frame(ll_caps, data[name])
}

# low high caps
lh_caps = data.frame(data[1:3])
for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_lh', sep="")
  lh_caps = data.frame(lh_caps, data[name])
}

# high low caps
hl_caps = data.frame(data[1:3])
for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_hl', sep="")
  hl_caps = data.frame(hl_caps, data[name])
}

# high high caps
hh_caps = data.frame(data[1:3])
for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_hh', sep="")
  hh_caps = data.frame(hh_caps, data[name])
}



#calc frequency for origin caps
origin_caps_frequency = data.frame(origin_caps[1:3])
freq_table = 0
for(i in origin_caps[4:53]){
    freq= table(i)
    freq_table = rbind(freq_table, freq)
}

rownames(freq_table) <- matrix(1:51)

