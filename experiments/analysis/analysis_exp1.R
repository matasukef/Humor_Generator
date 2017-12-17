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
summary(cap_scores_mean)
each_cap_mean = apply(cap_scores_mean, MARGIN=2, mean)




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


# calculate frequency of each similarities

#calc frequency for origin caps
origin_count = c()
for(i in 1:23){
  origin_count = append(origin_count, as.numeric(origin_caps[i, 4:53]))
}
origin_freq = table(origin_count)

#calc frequency for low low caption
ll_count = c()
for(i in 1:23){
  ll_count = append(ll_count, as.numeric(ll_caps[i, 4:53]))
}
ll_freq = table(ll_count)


#calc frequency for low high caption
lh_count = c()
for(i in 1:23){
  lh_count = append(lh_count, as.numeric(lh_caps[i, 4:53]))
}
lh_freq = table(lh_count)


#calc frequency for high low caption
hl_count = c()
for(i in 1:23){
  hl_count = append(hl_count, as.numeric(hl_caps[i, 4:53]))
}
hl_freq = table(hl_count)


#calc frequency for high high caption
hh_count = c()
for(i in 1:23){
  hh_count = append(hh_count, as.numeric(hh_caps[i, 4:53]))
}
hh_freq = table(hh_count)


# create each freq barplot
par(mfrow=c(3,2))
barplot(origin_freq, main="Baseline captions", xlab="Scores(Baseline)" , ylab="Frequency", ylim=c(0,700))
barplot(ll_freq, main="LL captions", xlab="Scores(LL Captions)" , ylab="Frequency", ylim=c(0,700))
barplot(lh_freq, main="LH captions", xlab="Scores(LH Captions)" , ylab="Frequency", ylim=c(0,700))
barplot(hl_freq, main="HL captions", xlab="Scores(HL Captions)" , ylab="Frequency", ylim=c(0,700))
barplot(hh_freq, main="HH captions", xlab="Scores(HH Captions)" , ylab="Frequency", ylim=c(0,700))






