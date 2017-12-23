setwd('~/../../../media/matasuke/Ubuntu01/Projects/Humor_Generator/experiments/analysis/data/exp1_with_original_caps_and_animals/')
exp1 <- read.csv('exp1_result.csv')
pre_survey <- read.csv('pre_survey_result.csv')


#extract data which age is distributed from 20 to 29.
# row 6 canavo and 24 REMINDER62 are seems to not to be used. because her score distribution is not goold. scores for original caption is highter than other caps.
exp1 = exp1[c(1:4, 7:8, 10:14, 16:23),]
pre_survey = pre_survey[c(1:2, 4:6, 8:13, 16:18, 21:25, 27:28), ]


SQH_score <- apply(pre_survey[4:7], MARGIN=1, sum)
MSHS_score <- apply(pre_survey[8:11], MARGIN=1, sum)

pre_survey_scores <- cbind(pre_survey[0:3], SQH_score, MSHS_score)

# bind scores with exp1
data <- merge(pre_survey_scores, exp1, by.x=c('age', 'name', 'sex'))

#merge result date with test_data
#merged_data = merge(data, test_data, by.x=c('image'))

EXP_NUM = 50
SUBJECT_NUM=19
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
# has to validate normality.
# 大数の法則により，正規分布になっているはず

cap_scores_mean = cap_scores_sum / EXP_NUM


#mean scores by col
summary(cap_scores_mean)
each_cap_mean = apply(cap_scores_mean, MARGIN=2, mean)

#boxplot
boxplot(cap_scores_mean)

#each sim mean scores per subjects
origin = cap_scores_mean$cap_origin
ll = cap_scores_mean$cap_ll
lh = cap_scores_mean$cap_lh
hl = cap_scores_mean$cap_hl
hh = cap_scores_mean$cap_hh





# mean of scores per each subject is inevitably based on normal distribution.
# so shapiro's test is not necessary.
shapiro.test(origin)
shapiro.test(ll)
shapiro.test(lh)
shapiro.test(hl)
shapiro.test(hh)

# Two factor analysis of variance
all_mean_data <- c(ll, lh, hl, hh)
img_sim <- factor(c(rep('画像高', 40), rep('画像低', 40)))
word_sim <- factor(rep(c(rep('単語高', 20), rep('単語低', 20)),2))
levels <- factor(rep(1:20, 4))
#summary(aov(all_mean_data))












# here just need to check difference between origin caps and hl captions.
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
for(i in 1:SUBJECT_NUM){
  origin_count = append(origin_count, as.numeric(origin_caps[i, 4:53]))
}
origin_freq = table(origin_count)

#calc frequency for low low caption
ll_count = c()
for(i in 1:SUBJECT_NUM){
  ll_count = append(ll_count, as.numeric(ll_caps[i, 4:53]))
}
ll_freq = table(ll_count)


#calc frequency for low high caption
lh_count = c()
for(i in 1:SUBJECT_NUM){
  lh_count = append(lh_count, as.numeric(lh_caps[i, 4:53]))
}
lh_freq = table(lh_count)


#calc frequency for high low caption
hl_count = c()
for(i in 1:SUBJECT_NUM){
  hl_count = append(hl_count, as.numeric(hl_caps[i, 4:53]))
}
hl_freq = table(hl_count)


#calc frequency for high high caption
hh_count = c()
for(i in 1:SUBJECT_NUM){
  hh_count = append(hh_count, as.numeric(hh_caps[i, 4:53]))
}
hh_freq = table(hh_count)


# create each freq barplot
#par(mfrow=c(3,2))
par(mfrow=c(1,2))
barplot(origin_freq, main="", xlab="Scores(Baseline)" , ylab="Frequency", ylim=c(0,800))
#barplot(ll_freq, main="LL captions", xlab="Scores(LL Captions)" , ylab="Frequency", ylim=c(0,1100))
#barplot(lh_freq, main="LH captions", xlab="Scores(LH Captions)" , ylab="Frequency", ylim=c(0,1100))
barplot(hl_freq, main="", xlab="Scores(Proposed method)" , ylab="Frequency", ylim=c(0,800))
#barplot(hh_freq, main="HH captions", xlab="Scores(HH Captions)" , ylab="Frequency", ylim=c(0,1100))

#friedman test and Wilcoxon signed rank test
#install.packages("exactRankTests", repos="http://cran.ism.ac.jp/")
library(exactRankTests)

#calculate each median.
humor_scores_origin = data.frame(data[1:5])
for(j in 1:EXP_NUM){
  name = paste('exp1_q', j, '_origin', sep="")
  humor_scores_origin = merge(humor_scores_origin, data[name])
}
humor_scores_origin = data.frame(humor_scores, score)



#friedman.test(y=matrix(c(ll, lh, hl, hh),ncol=4))
wilcox.exact(x=origin,y=ll,paired=T) # No difference between origin cap and ll cap.
wilcox.exact(x=origin,y=lh,paired=T) # No difference between origin cap and lh cap.
wilcox.exact(x=origin,y=hl,paired=T) # there is difference between origin cap and hl cap.
wilcox.exact(x=origin,y=hh,paired=T) # there is difference between origin cap and hh cap.
wilcox.exact(x=ll,y=lh,paired=T) # No difference between ll cap and lh cap.
wilcox.exact(x=ll,y=hl,paired=T) # there is difference between ll cap and hl cap.
wilcox.exact(x=ll,y=hh,paired=T) # No firrerence between ll cap and hh cap.
wilcox.exact(x=lh,y=hl,paired=T) # There is difference between lh cap and hl cap.
wilcox.exact(x=lh,y=hh,paired=T) # There is difference between lh cap and hh.
wilcox.exact(x=hl,y=hh,paired=T) # No difference between hl cap and hh cap.

#create plot for each subjects