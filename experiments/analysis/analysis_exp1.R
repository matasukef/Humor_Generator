setwd('~/../../../media/matasuke/Ubuntu01/Projects/Humor_Generator/experiments/analysis/data/exp1_with_original_caps_and_animals/')
exp1 <- read.csv('exp1_result.csv')
pre_survey <- read.csv('pre_survey_result.csv')

proposed_data <- read.csv('experiment1.csv')
images <- proposed_data[c(2, 9:20)]

#extract data which age is distributed from 20 to 29.



SQH_score <- apply(pre_survey[4:7], MARGIN=1, sum)
MSHS_score <- apply(pre_survey[8:11], MARGIN=1, sum)

pre_survey_scores <- cbind(pre_survey[0:3], SQH_score, MSHS_score)

# bind scores with exp1
data <- merge(pre_survey_scores, exp1, by.x=c('age', 'name', 'sex'))

#remove data which age is more than 30.
data = subset(data, data$age < 30)

# row 6 canavo and 24 REMINDER62 are seems to not to be used
#because her score distribution is not goold. scores for original caption is highter than other caps.
#data = subset(data, data$name != 'REMINDER62' & data$name != 'canavo' & data$name != 'happyturnkulukulri' & data$name != 'sayaka.am' & data$name != 'りんちゃん☆')
#data = subset(data, data$name != 'happyturnkulukulri' & data$name != 'REMINDER62' & data$name != 'canavo')
data = subset(data, data$name != 'happyturnkulukulri')
#merge result date with test_data
#merged_data = merge(data, test_data, by.x=c('image'))

EXP_NUM = 50
SUBJECT_NUM=length(data[,1])
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
par(mfrow=c(1,1))
#boxplot(cap_scores_mean, names=c('baseline', 'LL caption', 'LH caption', 'HL caption', 'HH caption'), xlab="Captions", ylab="mean scores", ylim=c(1,4))
boxplot(cap_scores_mean[2:5], names=c('LL caption', 'LH caption', 'HL caption', 'HH caption'), xlab="Captions", ylab="mean scores", ylim=c(1,4))
#each sim mean scores per subjects
origin = cap_scores_mean$cap_origin
ll = cap_scores_mean$cap_ll
lh = cap_scores_mean$cap_lh
hl = cap_scores_mean$cap_hl
hh = cap_scores_mean$cap_hh


# Two factor analysis of variance
all_mean_data <- c(ll, lh, hl, hh)
img_sim <- factor(c(rep('画像高', SUBJECT_NUM*2), rep('画像低', SUBJECT_NUM*2)))
word_sim <- factor(rep(c(rep('単語高', SUBJECT_NUM), rep('単語低', SUBJECT_NUM)),2))
levels <- factor(rep(1:SUBJECT_NUM, 4))
summary(aov(all_mean_data~img_sim*word_sim+Error(levels+levels:img_sim+levels:word_sim+levels:img_sim:word_sim)))

# bonferroni only img sim
ll_and_lh_data <- c(ll, lh)
hl_and_hh_data <- c(hl, hh)
ll_and_hl_data <- c(ll, hl)
lh_and_hh_data <- c(lh, hh)
t.test(ll_and_lh_data, hl_and_hh_data, paired=TRUE)
t.test(ll_and_hl_data, lh_and_hh_data, paired=TRUE)


#bonferroni 
#group <- factor(c(rep('LL',SUBJECT_NUM),rep('LH', SUBJECT_NUM), rep('HL', SUBJECT_NUM), rep('HH', SUBJECT_NUM)))
#pairwise.t.test(all_mean_data, group , p.adj = "bonf")


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
par(mfrow=c(3,2))
#par(mfrow=c(1,2))
barplot(origin_freq, main="Baseline", xlab="Scores(Baseline)" , ylab="Frequency", ylim=c(0,800))
barplot(ll_freq, main="LL captions", xlab="Scores(LL Captions)" , ylab="Frequency", ylim=c(0,800))
barplot(lh_freq, main="LH captions", xlab="Scores(LH Captions)" , ylab="Frequency", ylim=c(0,800))
barplot(hl_freq, main="HL captions", xlab="Scores(Proposed method)" , ylab="Frequency", ylim=c(0,800))
barplot(hh_freq, main="HH captions", xlab="Scores(HH Captions)" , ylab="Frequency", ylim=c(0,800))

#friedman test and Wilcoxon signed rank test
#install.packages("exactRankTests", repos="http://cran.ism.ac.jp/")
library(exactRankTests)

#calculate each median.
origin_caps_median = apply(origin_caps[4:53], MARGIN=1, median)
ll_caps_median = apply(ll_caps[4:53], MARGIN=1, median)
lh_caps_median = apply(lh_caps[4:53], MARGIN=1, median)
hl_caps_median = apply(hl_caps[4:53], MARGIN=1, median)
hh_caps_median = apply(hh_caps[4:53], MARGIN=1, median)
all_median_data <- c(ll_caps_median, lh_caps_median, hl_caps_median, hh_caps_median)

wilcox.exact(x=origin_caps_median,y=hl_caps_median,paired=T)

img_high_sim_median = (hl_caps_median + hh_caps_median) / 2
wilcox.exact(x=origin_caps_median, y=img_high_sim_median, paired=T)

#wilcox.exact(x=origin_caps_median,y=hl_caps_median,paired=T)
wilcox.exact(x=origin,y=hl,paired=T) # there is difference between origin cap and hl cap.


wilcox.exact(x=origin,y=ll,paired=T)
wilcox.exact(x=origin,y=lh,paired=T)
wilcox.exact(x=origin,y=hl,paired=T)
wilcox.exact(x=origin,y=hh,paired=T)
wilcox.exact(x=ll,y=lh,paired=T) # no difference
wilcox.exact(x=ll,y=hl,paired=T) # p < 0.1
wilcox.exact(x=ll,y=hh,paired=T) # no difference
wilcox.exact(x=lh,y=hl,paired=T) # no difference
wilcox.exact(x=lh,y=hh,paired=T)
wilcox.exact(x=hl,y=hh,paired=T)

#create plot for each subjects





#------------------------------------------------------------------------------------------------------------------------#
# cor
ll_humor_score = images['ll_humor_score']
ll_img_sim = images['ll_img_sim']
ll_word_sim = images['ll_word_sim']
each_ll_mean_score = as.numeric(apply(ll_caps[4:53], MARGIN=2, mean))
cor(ll_img_sim, each_ll_mean_score)
cor(ll_word_sim, each_ll_mean_score)
cor(hl_humor_score, each_ll_mean_score)

lh_humor_score = images['lh_humor_score']
lh_img_sim = images['lh_img_sim']
lh_word_sim = images['lh_word_sim']
each_lh_mean_score = as.numeric(apply(lh_caps[4:53], MARGIN=2, mean))
cor(lh_img_sim, each_lh_mean_score)
cor(lh_word_sim, each_lh_mean_score)
cor(lh_humor_score, each_lh_mean_score)

hl_humor_score = images['hl_humor_score']
hl_img_sim  = images['hl_img_sim']
hl_word_sim = images['hl_word_sim']
each_hl_mean_score = as.numeric(apply(hl_caps[4:53], MARGIN=2, mean))
cor(hl_img_sim, each_hl_mean_score)
cor(hl_word_sim, each_hl_mean_score)
cor(hl_humor_score, each_hl_mean_score)

hh_humor_score = images['hh_humor_score']
hh_img_sim = images['hh_img_sim']
hh_word_sim = images['hh_word_sim']
each_hh_mean_score = as.numeric(apply(hh_caps[4:53], MARGIN=2, mean))
cor(hh_humor_score, each_hh_mean_score)
cor(hh_img_sim, each_hh_mean_score)
cor(hh_word_sim, each_hh_mean_score)


# calc scores based on img sim
all_scores <- c(each_ll_mean_score, each_lh_mean_score, each_hl_mean_score, each_hh_mean_score)
all_humor_scores <- c(ll_humor_score[,1], lh_humor_score[,1], hl_humor_score[,1], hh_humor_score[,1])
all_img_sim <- c(ll_img_sim[,1], lh_img_sim[,1], hl_img_sim[,1], hh_img_sim[,1])
all_word_sim <- c(ll_word_sim[,1], lh_word_sim[,1], hl_word_sim[,1], hh_word_sim[,1])
cor(all_scores, all_img_sim)
cor(all_scores, all_word_sim)
cor(all_scores, all_humor_scores)

plot(all_scores, all_img_sim)
plot(all_scores, all_word_sim)
plot(all_scores, all_humor_scores)

#-------------------------------------------------------------------------------------------------------------------#

#each mean sim scores by images.
origin_scores = apply(origin_caps[4:53], MARGIN=2, mean)
ll_scores = apply(ll_caps[4:53], MARGIN=2, mean)
lh_scores = apply(lh_caps[4:53], MARGIN=2, mean)
hl_scores = apply(hl_caps[4:53], MARGIN=2, mean) # q12 is max
hh_scores = apply(hh_caps[4:53], MARGIN=2, mean) # q10 is max
plot(origin_scores)
plot(ll_scores)
plot(lh_scores)
plot(hl_scores)
plot(hh_scores)








#-----------------------------------------------------------------------------------------------#

#based on SQH and MSHS scores
SQH_low_group = subset(humor_scores, humor_scores$SQH_score <= 8)
SQH_high_group = subset(humor_scores, humor_scores$SQH_score >= 9)
MSHS_low_group = subset(humor_scores, humor_scores$MSHS_score <= 15)
MSHS_high_group = subset(humor_scores, humor_scores$MSHS_score >= 16)



# has to validate normality.
# 大数の法則により，正規分布になっているはず
par(mfrow=c(2,2))

sqh_low_group_scores_mean = SQH_low_group[6:10] / EXP_NUM
SQH_low_group_mean = cbind(SQH_low_group[1:5], sqh_low_group_scores_mean)
summary(SQH_low_group_mean[6:10])
boxplot(SQH_low_group_mean[6:10], main="SQH low group", names=c('baseline', 'LL caption', 'LH caption', 'HL caption', 'HH caption'), xlab="Captions", ylab="mean scores")

sqh_high_group_scores_mean = SQH_high_group[6:10] / EXP_NUM
SQH_high_group_mean = cbind(SQH_high_group[1:5], sqh_high_group_scores_mean)
summary(SQH_high_group_mean[6:10])
boxplot(SQH_high_group_mean[6:10], main="SQH high group", names=c('baseline', 'LL caption', 'LH caption', 'HL caption', 'HH caption'), xlab="Captions", ylab="mean scores")

MSHS_low_group_scores_mean = MSHS_low_group[6:10] / EXP_NUM
MSHS_low_group_mean = cbind(MSHS_low_group[1:5], MSHS_low_group_scores_mean)
summary(MSHS_low_group_mean[6:10])
boxplot(MSHS_low_group_mean[6:10], main="MSHS low group", names=c('baseline', 'LL caption', 'LH caption', 'HL caption', 'HH caption'), xlab="Captions", ylab="mean scores")

MSHS_high_group_scores_mean = MSHS_high_group[6:10] / EXP_NUM
MSHS_high_group_mean = cbind(MSHS_high_group[1:5], MSHS_high_group_scores_mean)
summary(MSHS_high_group_mean[6:10])
boxplot(MSHS_high_group_mean[6:10], main="MSHS high group", names=c('baseline', 'LL caption', 'LH caption', 'HL caption', 'HH caption'), xlab="Captions", ylab="mean scores")


## SQH low group ---------------------------------------------------------------------------------------
#each sim mean scores per subjects
SQH_low_group_origin = SQH_low_group_mean[6:10]$cap_origin
SQH_low_group_ll = SQH_low_group_mean[6:10]$cap_ll
SQH_low_group_lh = SQH_low_group_mean[6:10]$cap_lh
SQH_low_group_hl = SQH_low_group_mean[6:10]$cap_hl
SQH_low_group_hh = SQH_low_group_mean[6:10]$cap_hh

SQH_LOW_SUBJECT_NUM=length(SQH_low_group[,1])

# Two factor analysis of variance
SQH_low_group_all_mean_data <- c(SQH_low_group_ll, SQH_low_group_lh, SQH_low_group_hl, SQH_low_group_hh)
img_sim <- factor(c(rep('画像高', SQH_LOW_SUBJECT_NUM*2), rep('画像低', SQH_LOW_SUBJECT_NUM*2)))
word_sim <- factor(rep(c(rep('単語高', SQH_LOW_SUBJECT_NUM), rep('単語低', SQH_LOW_SUBJECT_NUM)),2))
levels <- factor(rep(1:SQH_LOW_SUBJECT_NUM, 4))
summary(aov(SQH_low_group_all_mean_data~img_sim*word_sim+Error(levels+levels:img_sim+levels:word_sim+levels:img_sim:word_sim)))

#----------------------------------------------------------------------------------------------------------

## SQH high group-----------------------------------------------------------------------------------------

#each sim mean scores per subjects
SQH_high_group_origin = SQH_high_group_mean[6:10]$cap_origin
SQH_high_group_ll = SQH_high_group_mean[6:10]$cap_ll
SQH_high_group_lh = SQH_high_group_mean[6:10]$cap_lh
SQH_high_group_hl = SQH_high_group_mean[6:10]$cap_hl
SQH_high_group_hh = SQH_high_group_mean[6:10]$cap_hh

SQH_HIGH_SUBJECT_NUM=length(SQH_high_group[,1])

# Two factor analysis of variance
SQH_high_group_all_mean_data <- c(SQH_high_group_ll, SQH_high_group_lh, SQH_high_group_hl, SQH_high_group_hh)
img_sim <- factor(c(rep('画像高', SQH_HIGH_SUBJECT_NUM*2), rep('画像低', SQH_HIGH_SUBJECT_NUM*2)))
word_sim <- factor(rep(c(rep('単語高', SQH_HIGH_SUBJECT_NUM), rep('単語低', SQH_HIGH_SUBJECT_NUM)),2))
levels <- factor(rep(1:SQH_HIGH_SUBJECT_NUM, 4))
summary(aov(SQH_high_group_all_mean_data~img_sim*word_sim+Error(levels+levels:img_sim+levels:word_sim+levels:img_sim:word_sim)))


#---------------------------------------------------------------------------------------------------------

## SQH low group ---------------------------------------------------------------------------------------
#each sim mean scores per subjects
MSHS_low_group_origin = MSHS_low_group_mean[6:10]$cap_origin
MSHS_low_group_ll = MSHS_low_group_mean[6:10]$cap_ll
MSHS_low_group_lh = MSHS_low_group_mean[6:10]$cap_lh
MSHS_low_group_hl = MSHS_low_group_mean[6:10]$cap_hl
MSHS_low_group_hh = MSHS_low_group_mean[6:10]$cap_hh

MSHS_LOW_SUBJECT_NUM=length(MSHS_low_group[,1])

# Two factor analysis of variance
MSHS_low_group_all_mean_data <- c(MSHS_low_group_ll, MSHS_low_group_lh, MSHS_low_group_hl, MSHS_low_group_hh)
img_sim <- factor(c(rep('画像高', MSHS_LOW_SUBJECT_NUM*2), rep('画像低', MSHS_LOW_SUBJECT_NUM*2)))
word_sim <- factor(rep(c(rep('単語高', MSHS_LOW_SUBJECT_NUM), rep('単語低', MSHS_LOW_SUBJECT_NUM)),2))
levels <- factor(rep(1:MSHS_LOW_SUBJECT_NUM, 4))
summary(aov(MSHS_low_group_all_mean_data~img_sim*word_sim+Error(levels+levels:img_sim+levels:word_sim+levels:img_sim:word_sim)))

#----------------------------------------------------------------------------------------------------------

## SQH low group ---------------------------------------------------------------------------------------
#each sim mean scores per subjects
MSHS_high_group_origin = MSHS_high_group_mean[6:10]$cap_origin
MSHS_high_group_ll = MSHS_high_group_mean[6:10]$cap_ll
MSHS_high_group_lh = MSHS_high_group_mean[6:10]$cap_lh
MSHS_high_group_hl = MSHS_high_group_mean[6:10]$cap_hl
MSHS_high_group_hh = MSHS_high_group_mean[6:10]$cap_hh

MSHS_HIGH_SUBJECT_NUM=length(MSHS_high_group[,1])

# Two factor analysis of variance
MSHS_high_group_all_mean_data <- c(MSHS_high_group_ll, MSHS_high_group_lh, MSHS_high_group_hl, MSHS_high_group_hh)
img_sim <- factor(c(rep('画像高', MSHS_HIGH_SUBJECT_NUM*2), rep('画像低', MSHS_HIGH_SUBJECT_NUM*2)))
word_sim <- factor(rep(c(rep('単語高', MSHS_HIGH_SUBJECT_NUM), rep('単語低', MSHS_HIGH_SUBJECT_NUM)),2))
levels <- factor(rep(1:MSHS_HIGH_SUBJECT_NUM, 4))
summary(aov(MSHS_high_group_all_mean_data~img_sim*word_sim+Error(levels+levels:img_sim+levels:word_sim+levels:img_sim:word_sim)))

#----------------------------------------------------------------------------------------------------------



#SQH high and MSHS low
SQH_high_and_MSHS_high_group = subset(SQH_high_group, SQH_high_group$MSHS_score >= 16)

SQH_high_and_MSHS_high_group_scores_mean = SQH_high_and_MSHS_high_group[6:10] / EXP_NUM
SQH_high_and_MSHS_high_group_mean = cbind(SQH_high_and_MSHS_high_group[1:5], SQH_high_and_MSHS_high_group_scores_mean)
summary(SQH_high_and_MSHS_high_group_mean[6:10])
boxplot(SQH_high_and_MSHS_high_group_mean[6:10], main="SQH high and SHSQ high group", names=c('baseline', 'LL caption', 'LH caption', 'HL caption', 'HH caption'), xlab="Captions", ylab="mean scores")

SQH_high_and_MSHS_high_group_origin = SQH_high_and_MSHS_high_group_mean[6:10]$cap_origin
SQH_high_and_MSHS_high_group_ll = SQH_high_and_MSHS_high_group_mean[6:10]$cap_ll
SQH_high_and_MSHS_high_group_lh = SQH_high_and_MSHS_high_group_mean[6:10]$cap_lh
SQH_high_and_MSHS_high_group_hl = SQH_high_and_MSHS_high_group_mean[6:10]$cap_hl
SQH_high_and_MSHS_high_group_hh = SQH_high_and_MSHS_high_group_mean[6:10]$cap_hh

SQH_HIGH_AND_MSHS_HIGH_SUBJECT_NUM=length(SQH_high_and_MSHS_high_group[,1])

# Two factor analysis of variance
SQH_high_and_MSHS_high_group_all_mean_data <- c(SQH_high_and_MSHS_high_group_ll, SQH_high_and_MSHS_high_group_lh, SQH_high_and_MSHS_high_group_hl, SQH_high_and_MSHS_high_group_hh)
img_sim <- factor(c(rep('画像高', SQH_HIGH_AND_MSHS_HIGH_SUBJECT_NUM*2), rep('画像低', SQH_HIGH_AND_MSHS_HIGH_SUBJECT_NUM*2)))
word_sim <- factor(rep(c(rep('単語高', SQH_HIGH_AND_MSHS_HIGH_SUBJECT_NUM), rep('単語低', SQH_HIGH_AND_MSHS_HIGH_SUBJECT_NUM)),2))
levels <- factor(rep(1:SQH_HIGH_AND_MSHS_HIGH_SUBJECT_NUM, 4))
summary(aov(SQH_high_and_MSHS_high_group_all_mean_data~img_sim*word_sim+Error(levels+levels:img_sim+levels:word_sim+levels:img_sim:word_sim)))






#画像間類似度はユーモアの受容性に還元していることが判明したため，高画像間類似度のものだけで再検定

3,4,10, 13, 15, 16, 20, 21, 23, 29, 33, 34, 39, 43, 44

humor_scores_high_img_sim_ones = data.frame(data[1:5])
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

