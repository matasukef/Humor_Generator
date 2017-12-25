setwd('~/../../../media/matasuke/Ubuntu01/Projects/Humor_Generator/experiments/analysis/data/exp1_with_original_caps_and_animals/')
exp1 <- read.csv('exp1_result.csv')
pre_survey <- read.csv('pre_survey_result.csv')

proposed_data <- read.csv('experiment1.csv')
images <- proposed_data[c(2, 9:20)]

SQH_score <- apply(pre_survey[4:7], MARGIN=1, sum)
MSHS_score <- apply(pre_survey[8:11], MARGIN=1, sum)
pre_survey_scores <- cbind(pre_survey[0:3], SQH_score, MSHS_score)

# bind scores with exp1
data <- merge(pre_survey_scores, exp1, by.x=c('age', 'name', 'sex'))

#remove data which age is more than 30.
data = subset(data, data$age < 30)

# row 6 canavo and 24 REMINDER62 are seems to not to be used
#because her score distribution is not goold. scores for original caption is highter than other caps.
data = subset(data, data$name != 'happyturnkulukulri' )

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
boxplot(cap_scores_mean, names=c('baseline', 'LL caption', 'LH caption', 'HL caption', 'HH caption'), xlab="Captions", ylab="mean scores", ylim=c(1,4))


#origin = cap_scores_mean$cap_origin
#ll = cap_scores_mean$cap_ll
#lh = cap_scores_mean$cap_lh
#hl = cap_scores_mean$cap_hl
#hh = cap_scores_mean$cap_hh

# Two factor analysis of variance
#all_mean_data <- c(ll, lh, hl, hh)
#img_sim <- factor(c(rep('画像高', SUBJECT_NUM*2), rep('画像低', SUBJECT_NUM*2)))
#word_sim <- factor(rep(c(rep('単語高', SUBJECT_NUM), rep('単語低', SUBJECT_NUM)),2))
#levels <- factor(rep(1:SUBJECT_NUM, 4))
#summary(aov(all_mean_data~img_sim*word_sim+Error(levels+levels:img_sim+levels:word_sim+levels:img_sim:word_sim)))


# here just need to check difference between origin caps and hl captions.
# origin caps
origin_caps = data.frame(data[1:3])
ll_caps = data.frame(data[1:3])
lh_caps = data.frame(data[1:3])
hl_caps = data.frame(data[1:3])
hh_caps = data.frame(data[1:3])
for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_origin', sep="")
  origin_caps = data.frame(origin_caps, data[name])
  
  name = paste('exp1_q', i, '_ll', sep="")
  ll_caps = data.frame(ll_caps, data[name])
  
  name = paste('exp1_q', i, '_lh', sep="")
  lh_caps = data.frame(lh_caps, data[name])
  
  name = paste('exp1_q', i, '_hl', sep="")
  hl_caps = data.frame(hl_caps, data[name])
  
  name = paste('exp1_q', i, '_hh', sep="")
  hh_caps = data.frame(hh_caps, data[name])
}


# calculate frequency of each similarities
origin_count = c()
ll_count = c()
lh_count = c()
hl_count = c()
hh_count = c()
for(i in 1:SUBJECT_NUM){
  origin_count = append(origin_count, as.numeric(origin_caps[i, 4:53]))
  ll_count = append(ll_count, as.numeric(ll_caps[i, 4:53]))
  lh_count = append(lh_count, as.numeric(lh_caps[i, 4:53]))
  hl_count = append(hl_count, as.numeric(hl_caps[i, 4:53]))
  hh_count = append(hh_count, as.numeric(hh_caps[i, 4:53]))
}
origin_freq = table(origin_count)
ll_freq = table(ll_count)
lh_freq = table(lh_count)
hl_freq = table(hl_count)
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


#create list to collect each sims scores for all subjects.

origin_all_scores = c()
ll_all_scores = c()
lh_all_scores = c()
hl_all_scores = c()
hh_all_scores = c()
for(i in 4:length(origin_caps)){
  origin_all_scores = c(origin_all_scores, origin_caps[,i])
  ll_all_scores = c(ll_all_scores, ll_caps[,i])
  lh_all_scores = c(lh_all_scores, lh_caps[,i])
  hl_all_scores = c(hl_all_scores, hl_caps[,i])
  hh_all_scores = c(hh_all_scores, hh_caps[,i])
}



# calculate wilcox.exact by above data
wilcox.exact(x=origin_all_scores,y=ll_all_scores,paired=T)　# there is difference
wilcox.exact(x=origin_all_scores,y=lh_all_scores,paired=T)　# there is difference
wilcox.exact(x=origin_all_scores,y=hl_all_scores,paired=T)　# there is difference
wilcox.exact(x=origin_all_scores,y=hh_all_scores,paired=T)　# there is difference
wilcox.exact(x=ll_all_scores,y=lh_all_scores,paired=T) # No difference
wilcox.exact(x=ll_all_scores,y=hl_all_scores,paired=T) # there is difference between ll caps and hl caps p < 0.01
wilcox.exact(x=ll_all_scores,y=hh_all_scores,paired=T) # No difference
wilcox.exact(x=lh_all_scores,y=hl_all_scores,paired=T) # there is difference between lh caps and hl caps p < 0.01
wilcox.exact(x=lh_all_scores,y=hh_all_scores,paired=T) # No difference
wilcox.exact(x=hl_all_scores,y=hh_all_scores,paired=T) # No difference


# Original captionｔとその他提案手法を含むcaption間では有意な差が見られたため，只のキャプションを提示するよりは，
# ユーザーのユーモア受容性が向上すると明らかになった

# その他のキャプションについては，LL caption と LH caption間で5%ｓ水準で有意な差があったため，画像間類似度がユーモアの受容性に関連する
# HL captionと HH captionに関しても 1%水準で有意な差があったため，単語間類似度がユーモアの受容性に関連する

#------------------------------------------------------------------------------------------------------------------------#
# cor
ll_humor_score = images['ll_humor_score']
ll_img_sim = images['ll_img_sim']
ll_word_sim = images['ll_word_sim']
each_ll_mean_score = as.numeric(apply(ll_caps[4:53], MARGIN=2, mean))
cor(ll_img_sim, each_ll_mean_score)
cor(ll_word_sim, each_ll_mean_score)
cor(ll_humor_score, each_ll_mean_score)


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
par(mfrow=c(3,2))
barplot(origin_scores)
barplot(ll_scores)
barplot(lh_scores)
barplot(hl_scores)
barplot(hh_scores)

max(hl_scores)
max(hh_scores)




#analize based on SQH and MSHS scores-----------------------------------------------------------------------------------#

#based on SQH and MSHS scores
SQH_low_group = subset(humor_scores, humor_scores$SQH_score <= 8)
SQH_high_group = subset(humor_scores, humor_scores$SQH_score >= 9)
MSHS_low_group = subset(humor_scores, humor_scores$MSHS_score <= 17)
MSHS_high_group = subset(humor_scores, humor_scores$MSHS_score >= 18)


# has to validate normality.
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


# all data based on SQH and MSHS scores
SQH_low_group_data = subset(data, data$SQH_score <= 8)
SQH_high_group_data = subset(data, data$SQH_score >= 9)
MSHS_low_group_data = subset(data, data$MSHS_score <= 15)
MSHS_high_group_data = subset(data, data$MSHS_score >= 16)


## SQH low group ---------------------------------------------------------------------------------------
#each sim mean scores per subjects
SQH_LOW_SUBJECT_NUM=length(SQH_low_group_data[,1])

SQH_low_origin_caps = data.frame(SQH_low_group_data[1:3])
SQH_low_ll_caps = data.frame(SQH_low_group_data[1:3])
SQH_low_lh_caps = data.frame(SQH_low_group_data[1:3])
SQH_low_hl_caps = data.frame(SQH_low_group_data[1:3])
SQH_low_hh_caps = data.frame(SQH_low_group_data[1:3])
for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_origin', sep="")
  SQH_low_origin_caps = data.frame(SQH_low_origin_caps, SQH_low_group_data[name])
  
  name = paste('exp1_q', i, '_ll', sep="")
  SQH_low_ll_caps = data.frame(SQH_low_ll_caps, SQH_low_group_data[name])
  
  name = paste('exp1_q', i, '_lh', sep="")
  SQH_low_lh_caps = data.frame(SQH_low_lh_caps, SQH_low_group_data[name])
  
  name = paste('exp1_q', i, '_hl', sep="")
  SQH_low_hl_caps = data.frame(SQH_low_hl_caps, SQH_low_group_data[name])
  
  name = paste('exp1_q', i, '_hh', sep="")
  SQH_low_hh_caps = data.frame(SQH_low_hh_caps, SQH_low_group_data[name])
}


# calculate frequency of each similarities
SQH_low_origin_count = c()
SQH_low_ll_count = c()
SQH_low_lh_count = c()
SQH_low_hl_count = c()
SQH_low_hh_count = c()
for(i in 1:SQH_LOW_SUBJECT_NUM){
  SQH_low_origin_count = append(SQH_low_origin_count, as.numeric(SQH_low_origin_caps[i, 4:53]))
  SQH_low_ll_count = append(SQH_low_ll_count, as.numeric(SQH_low_ll_caps[i, 4:53]))
  SQH_low_lh_count = append(SQH_low_lh_count, as.numeric(SQH_low_lh_caps[i, 4:53]))
  SQH_low_hl_count = append(SQH_low_hl_count, as.numeric(SQH_low_hl_caps[i, 4:53]))
  SQH_low_hh_count = append(SQH_low_hh_count, as.numeric(SQH_low_hh_caps[i, 4:53]))
}
SQH_low_origin_freq = table(SQH_low_origin_count)
SQH_low_ll_freq = table(SQH_low_ll_count)
SQH_low_lh_freq = table(SQH_low_lh_count)
SQH_low_hl_freq = table(SQH_low_hl_count)
SQH_low_hh_freq = table(SQH_low_hh_count)


# create each freq barplot
par(mfrow=c(3,2))
#par(mfrow=c(1,2))
barplot(SQH_low_origin_freq, main="Baseline", xlab="Scores(Baseline)" , ylab="Frequency", ylim=c(0,800))
barplot(SQH_low_ll_freq, main="LL captions", xlab="Scores(LL Captions)" , ylab="Frequency", ylim=c(0,800))
barplot(SQH_low_lh_freq, main="LH captions", xlab="Scores(LH Captions)" , ylab="Frequency", ylim=c(0,800))
barplot(SQH_low_hl_freq, main="HL captions", xlab="Scores(Proposed method)" , ylab="Frequency", ylim=c(0,800))
barplot(SQH_low_hh_freq, main="HH captions", xlab="Scores(HH Captions)" , ylab="Frequency", ylim=c(0,800))


#create list to collect each sims scores for all subjects.

SQH_low_origin_all_scores = c()
SQH_low_ll_all_scores = c()
SQH_low_lh_all_scores = c()
SQH_low_hl_all_scores = c()
SQH_low_hh_all_scores = c()
for(i in 4:length(SQH_low_origin_caps)){
  SQH_low_origin_all_scores = c(SQH_low_origin_all_scores, SQH_low_origin_caps[,i])
  SQH_low_ll_all_scores = c(SQH_low_ll_all_scores, SQH_low_ll_caps[,i])
  SQH_low_lh_all_scores = c(SQH_low_lh_all_scores, SQH_low_lh_caps[,i])
  SQH_low_hl_all_scores = c(SQH_low_hl_all_scores, SQH_low_hl_caps[,i])
  SQH_low_hh_all_scores = c(SQH_low_hh_all_scores, SQH_low_hh_caps[,i])
}



# calculate wilcox.exact by above data
wilcox.exact(x=SQH_low_origin_all_scores,y=SQH_low_ll_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_low_origin_all_scores,y=SQH_low_lh_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_low_origin_all_scores,y=SQH_low_hl_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_low_origin_all_scores,y=SQH_low_hh_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_low_ll_all_scores,y=SQH_low_lh_all_scores,paired=T) # No difference
wilcox.exact(x=SQH_low_ll_all_scores,y=SQH_low_hl_all_scores,paired=T) # there is difference between ll caps and hl caps p < 0.01
wilcox.exact(x=SQH_low_ll_all_scores,y=SQH_low_hh_all_scores,paired=T) # No difference
wilcox.exact(x=SQH_low_lh_all_scores,y=SQH_low_hl_all_scores,paired=T) # there is difference between lh caps and hl caps p < 0.01
wilcox.exact(x=SQH_low_lh_all_scores,y=SQH_low_hh_all_scores,paired=T) # No difference
wilcox.exact(x=SQH_low_hl_all_scores,y=SQH_low_hh_all_scores,paired=T) # There is difference between hl caps and hh caps p < 0.05



#----------------------------------------------------------------------------------------------------------

## SQH high group-----------------------------------------------------------------------------------------

#each sim mean scores per subjects
SQH_HIGH_SUBJECT_NUM=length(SQH_high_group_data[,1])

SQH_high_origin_caps = data.frame(SQH_high_group_data[1:3])
SQH_high_ll_caps = data.frame(SQH_high_group_data[1:3])
SQH_high_lh_caps = data.frame(SQH_high_group_data[1:3])
SQH_high_hl_caps = data.frame(SQH_high_group_data[1:3])
SQH_high_hh_caps = data.frame(SQH_high_group_data[1:3])

for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_origin', sep="")
  SQH_high_origin_caps = data.frame(SQH_high_origin_caps, SQH_high_group_data[name])
  
  name = paste('exp1_q', i, '_ll', sep="")
  SQH_high_ll_caps = data.frame(SQH_high_ll_caps, SQH_high_group_data[name])
  
  name = paste('exp1_q', i, '_lh', sep="")
  SQH_high_lh_caps = data.frame(SQH_high_lh_caps, SQH_high_group_data[name])
  
  name = paste('exp1_q', i, '_hl', sep="")
  SQH_high_hl_caps = data.frame(SQH_high_hl_caps, SQH_high_group_data[name])
  
  name = paste('exp1_q', i, '_hh', sep="")
  SQH_high_hh_caps = data.frame(SQH_high_hh_caps, SQH_high_group_data[name])
}

# calculate frequency of each similarities
SQH_high_origin_count = c()
SQH_high_ll_count = c()
SQH_high_lh_count = c()
SQH_high_hl_count = c()
SQH_high_hh_count = c()
for(i in 1:SQH_LOW_SUBJECT_NUM){
  SQH_high_origin_count = append(SQH_high_origin_count, as.numeric(SQH_high_origin_caps[i, 4:53]))
  SQH_high_ll_count = append(SQH_high_ll_count, as.numeric(SQH_high_ll_caps[i, 4:53]))
  SQH_high_lh_count = append(SQH_high_lh_count, as.numeric(SQH_high_lh_caps[i, 4:53]))
  SQH_high_hl_count = append(SQH_high_hl_count, as.numeric(SQH_high_hl_caps[i, 4:53]))
  SQH_high_hh_count = append(SQH_high_hh_count, as.numeric(SQH_high_hh_caps[i, 4:53]))
}
SQH_high_origin_freq = table(SQH_high_origin_count)
SQH_high_ll_freq = table(SQH_high_ll_count)
SQH_high_lh_freq = table(SQH_high_lh_count)
SQH_high_hl_freq = table(SQH_high_hl_count)
SQH_high_hh_freq = table(SQH_high_hh_count)


# create each freq barplot
par(mfrow=c(3,2))
barplot(SQH_high_origin_freq, main="Baseline", xlab="Scores(Baseline)", ylab="Frequency", ylim=c(0,800))
barplot(SQH_high_ll_freq, main="LL captions", xlab="Scores(LL Captions)", ylab="Frequency", ylim=c(0,800))
barplot(SQH_high_lh_freq, main="LH captions", xlab="Scores(LH Captions)", ylab="Frequency", ylim=c(0,800))
barplot(SQH_high_hl_freq, main="HL captions", xlab="Scores(Proposed method)", ylab="Frequency", ylim=c(0,800))
barplot(SQH_high_hh_freq, main="HH captions", xlab="Scores(HH Captions)", ylab="Frequency", ylim=c(0,800))


#create list to collect each sims scores for all subjects.

SQH_high_origin_all_scores = c()
SQH_high_ll_all_scores = c()
SQH_high_lh_all_scores = c()
SQH_high_hl_all_scores = c()
SQH_high_hh_all_scores = c()
for(i in 4:length(SQH_low_origin_caps)){
  SQH_high_origin_all_scores = c(SQH_high_origin_all_scores, SQH_high_origin_caps[,i])
  SQH_high_ll_all_scores = c(SQH_high_ll_all_scores, SQH_high_ll_caps[,i])
  SQH_high_lh_all_scores = c(SQH_high_lh_all_scores, SQH_high_lh_caps[,i])
  SQH_high_hl_all_scores = c(SQH_high_hl_all_scores, SQH_high_hl_caps[,i])
  SQH_high_hh_all_scores = c(SQH_high_hh_all_scores, SQH_high_hh_caps[,i])
}



# calculate wilcox.exact by above data
wilcox.exact(x=SQH_high_origin_all_scores,y=SQH_high_ll_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_high_origin_all_scores,y=SQH_high_lh_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_high_origin_all_scores,y=SQH_high_hl_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_high_origin_all_scores,y=SQH_high_hh_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_high_ll_all_scores,y=SQH_high_lh_all_scores,paired=T) # No difference
wilcox.exact(x=SQH_high_ll_all_scores,y=SQH_high_hl_all_scores,paired=T) # there is difference between ll caps and hl caps p < 0.01
wilcox.exact(x=SQH_high_ll_all_scores,y=SQH_high_hh_all_scores,paired=T) # No difference
wilcox.exact(x=SQH_high_lh_all_scores,y=SQH_high_hl_all_scores,paired=T) # there is difference between lh caps and hl caps p < 0.01
wilcox.exact(x=SQH_high_lh_all_scores,y=SQH_high_hh_all_scores,paired=T) # No difference
wilcox.exact(x=SQH_high_hl_all_scores,y=SQH_high_hh_all_scores,paired=T) # There is difference between hl caps and hh caps p < 0.05





#---------------------------------------------------------------------------------------------------------

## MSHS low group ---------------------------------------------------------------------------------------
#each sim mean scores per subjects
MSHS_LOW_SUBJECT_NUM=length(MSHS_low_group_data[,1])

MSHS_low_origin_caps = data.frame(MSHS_low_group_data[1:3])
MSHS_low_ll_caps = data.frame(MSHS_low_group_data[1:3])
MSHS_low_lh_caps = data.frame(MSHS_low_group_data[1:3])
MSHS_low_hl_caps = data.frame(MSHS_low_group_data[1:3])
MSHS_low_hh_caps = data.frame(MSHS_low_group_data[1:3])

for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_origin', sep="")
  MSHS_low_origin_caps = data.frame(MSHS_low_origin_caps, MSHS_low_group_data[name])
  
  name = paste('exp1_q', i, '_ll', sep="")
  MSHS_low_ll_caps = data.frame(MSHS_low_ll_caps, MSHS_low_group_data[name])
  
  name = paste('exp1_q', i, '_lh', sep="")
  MSHS_low_lh_caps = data.frame(MSHS_low_lh_caps, MSHS_low_group_data[name])
  
  name = paste('exp1_q', i, '_hl', sep="")
  MSHS_low_hl_caps = data.frame(MSHS_low_hl_caps, MSHS_low_group_data[name])
  
  name = paste('exp1_q', i, '_hh', sep="")
  MSHS_low_hh_caps = data.frame(MSHS_low_hh_caps, MSHS_low_group_data[name])
}


# calculate frequency of each similarities
MSHS_low_origin_count = c()
MSHS_low_ll_count = c()
MSHS_low_lh_count = c()
MSHS_low_hl_count = c()
MSHS_low_hh_count = c()
for(i in 1:MSHS_LOW_SUBJECT_NUM){
  MSHS_low_origin_count = append(MSHS_low_origin_count, as.numeric(MSHS_low_origin_caps[i, 4:53]))
  MSHS_low_ll_count = append(MSHS_low_ll_count, as.numeric(MSHS_low_ll_caps[i, 4:53]))
  MSHS_low_lh_count = append(MSHS_low_lh_count, as.numeric(MSHS_low_lh_caps[i, 4:53]))
  MSHS_low_hl_count = append(MSHS_low_hl_count, as.numeric(MSHS_low_hl_caps[i, 4:53]))
  MSHS_low_hh_count = append(MSHS_low_hh_count, as.numeric(MSHS_low_hh_caps[i, 4:53]))
}
MSHS_low_origin_freq = table(MSHS_low_origin_count)
MSHS_low_ll_freq = table(MSHS_low_ll_count)
MSHS_low_lh_freq = table(MSHS_low_lh_count)
MSHS_low_hl_freq = table(MSHS_low_hl_count)
MSHS_low_hh_freq = table(MSHS_low_hh_count)


# create each freq barplot
par(mfrow=c(3,2))
#par(mfrow=c(1,2))
barplot(MSHS_low_origin_freq, main="Baseline", xlab="Scores(Baseline)" , ylab="Frequency", ylim=c(0,800))
barplot(MSHS_low_ll_freq, main="LL captions", xlab="Scores(LL Captions)" , ylab="Frequency", ylim=c(0,800))
barplot(MSHS_low_lh_freq, main="LH captions", xlab="Scores(LH Captions)" , ylab="Frequency", ylim=c(0,800))
barplot(MSHS_low_hl_freq, main="HL captions", xlab="Scores(Proposed method)" , ylab="Frequency", ylim=c(0,800))
barplot(MSHS_low_hh_freq, main="HH captions", xlab="Scores(HH Captions)" , ylab="Frequency", ylim=c(0,800))


#create list to collect each sims scores for all subjects.

MSHS_low_origin_all_scores = c()
MSHS_low_ll_all_scores = c()
MSHS_low_lh_all_scores = c()
MSHS_low_hl_all_scores = c()
MSHS_low_hh_all_scores = c()
for(i in 4:length(MSHS_low_origin_caps)){
  MSHS_low_origin_all_scores = c(MSHS_low_origin_all_scores, MSHS_low_origin_caps[,i])
  MSHS_low_ll_all_scores = c(MSHS_low_ll_all_scores, MSHS_low_ll_caps[,i])
  MSHS_low_lh_all_scores = c(MSHS_low_lh_all_scores, MSHS_low_lh_caps[,i])
  MSHS_low_hl_all_scores = c(MSHS_low_hl_all_scores, MSHS_low_hl_caps[,i])
  MSHS_low_hh_all_scores = c(MSHS_low_hh_all_scores, MSHS_low_hh_caps[,i])
}



# calculate wilcox.exact by above data
wilcox.exact(x=MSHS_low_origin_all_scores, y=MSHS_low_ll_all_scores, paired=T)　# there is difference
wilcox.exact(x=MSHS_low_origin_all_scores, y=MSHS_low_lh_all_scores, paired=T)　# there is difference
wilcox.exact(x=MSHS_low_origin_all_scores, y=MSHS_low_hl_all_scores, paired=T)　# there is difference
wilcox.exact(x=MSHS_low_origin_all_scores, y=MSHS_low_hh_all_scores, paired=T)　# there is difference
wilcox.exact(x=MSHS_low_ll_all_scores, y=MSHS_low_lh_all_scores, paired=T) # No difference
wilcox.exact(x=MSHS_low_ll_all_scores, y=MSHS_low_hl_all_scores, paired=T) # there is difference between ll caps and hl caps p < 0.01
wilcox.exact(x=MSHS_low_ll_all_scores, y=MSHS_low_hh_all_scores, paired=T) # No difference
wilcox.exact(x=MSHS_low_lh_all_scores, y=MSHS_low_hl_all_scores, paired=T) # there is difference between lh caps and hl caps p < 0.01
wilcox.exact(x=MSHS_low_lh_all_scores, y=MSHS_low_hh_all_scores, paired=T) # No difference
wilcox.exact(x=MSHS_low_hl_all_scores, y=MSHS_low_hh_all_scores, paired=T) # There is difference between hl caps and hh caps p < 0.05


#----------------------------------------------------------------------------------------------------------

## MSHS high group ---------------------------------------------------------------------------------------

#each sim mean scores per subjects
MSHS_HIGH_SUBJECT_NUM=length(MSHS_high_group_data[,1])

MSHS_high_origin_caps = data.frame(MSHS_high_group_data[1:3])
MSHS_high_ll_caps = data.frame(MSHS_high_group_data[1:3])
MSHS_high_lh_caps = data.frame(MSHS_high_group_data[1:3])
MSHS_high_hl_caps = data.frame(MSHS_high_group_data[1:3])
MSHS_high_hh_caps = data.frame(MSHS_high_group_data[1:3])

for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_origin', sep="")
  MSHS_high_origin_caps = data.frame(MSHS_high_origin_caps, MSHS_high_group_data[name])
  
  name = paste('exp1_q', i, '_ll', sep="")
  MSHS_high_ll_caps = data.frame(MSHS_high_ll_caps, MSHS_high_group_data[name])
  
  name = paste('exp1_q', i, '_lh', sep="")
  MSHS_high_lh_caps = data.frame(MSHS_high_lh_caps, MSHS_high_group_data[name])
  
  name = paste('exp1_q', i, '_hl', sep="")
  MSHS_high_hl_caps = data.frame(MSHS_high_hl_caps, MSHS_high_group_data[name])
  
  name = paste('exp1_q', i, '_hh', sep="")
  MSHS_high_hh_caps = data.frame(MSHS_high_hh_caps, MSHS_high_group_data[name])
}

# calculate frequency of each similarities
MSHS_high_origin_count = c()
MSHS_high_ll_count = c()
MSHS_high_lh_count = c()
MSHS_high_hl_count = c()
MSHS_high_hh_count = c()
for(i in 1:MSHS_LOW_SUBJECT_NUM){
  MSHS_high_origin_count = append(MSHS_high_origin_count, as.numeric(MSHS_high_origin_caps[i, 4:53]))
  MSHS_high_ll_count = append(MSHS_high_ll_count, as.numeric(MSHS_high_ll_caps[i, 4:53]))
  MSHS_high_lh_count = append(MSHS_high_lh_count, as.numeric(MSHS_high_lh_caps[i, 4:53]))
  MSHS_high_hl_count = append(MSHS_high_hl_count, as.numeric(MSHS_high_hl_caps[i, 4:53]))
  MSHS_high_hh_count = append(MSHS_high_hh_count, as.numeric(MSHS_high_hh_caps[i, 4:53]))
}
MSHS_high_origin_freq = table(MSHS_high_origin_count)
MSHS_high_ll_freq = table(MSHS_high_ll_count)
MSHS_high_lh_freq = table(MSHS_high_lh_count)
MSHS_high_hl_freq = table(MSHS_high_hl_count)
MSHS_high_hh_freq = table(MSHS_high_hh_count)


# create each freq barplot
par(mfrow=c(3,2))
barplot(MSHS_high_origin_freq, main="Baseline", xlab="Scores(Baseline)", ylab="Frequency", ylim=c(0,800))
barplot(MSHS_high_ll_freq, main="LL captions", xlab="Scores(LL Captions)", ylab="Frequency", ylim=c(0,800))
barplot(MSHS_high_lh_freq, main="LH captions", xlab="Scores(LH Captions)", ylab="Frequency", ylim=c(0,800))
barplot(MSHS_high_hl_freq, main="HL captions", xlab="Scores(Proposed method)", ylab="Frequency", ylim=c(0,800))
barplot(MSHS_high_hh_freq, main="HH captions", xlab="Scores(HH Captions)", ylab="Frequency", ylim=c(0,800))


#create list to collect each sims scores for all subjects.

MSHS_high_origin_all_scores = c()
MSHS_high_ll_all_scores = c()
MSHS_high_lh_all_scores = c()
MSHS_high_hl_all_scores = c()
MSHS_high_hh_all_scores = c()
for(i in 4:length(MSHS_high_origin_caps)){
  MSHS_high_origin_all_scores = c(MSHS_high_origin_all_scores, MSHS_high_origin_caps[,i])
  MSHS_high_ll_all_scores = c(MSHS_high_ll_all_scores, MSHS_high_ll_caps[,i])
  MSHS_high_lh_all_scores = c(MSHS_high_lh_all_scores, MSHS_high_lh_caps[,i])
  MSHS_high_hl_all_scores = c(MSHS_high_hl_all_scores, MSHS_high_hl_caps[,i])
  MSHS_high_hh_all_scores = c(MSHS_high_hh_all_scores, MSHS_high_hh_caps[,i])
}



# calculate wilcox.exact by above data
wilcox.exact(x=MSHS_high_origin_all_scores,y=MSHS_high_ll_all_scores,paired=T)　# there is difference
wilcox.exact(x=MSHS_high_origin_all_scores,y=MSHS_high_lh_all_scores,paired=T)　# there is difference
wilcox.exact(x=MSHS_high_origin_all_scores,y=MSHS_high_hl_all_scores,paired=T)　# there is difference
wilcox.exact(x=MSHS_high_origin_all_scores,y=MSHS_high_hh_all_scores,paired=T)　# there is difference
wilcox.exact(x=MSHS_high_ll_all_scores,y=MSHS_high_lh_all_scores,paired=T) # No difference
wilcox.exact(x=MSHS_high_ll_all_scores,y=MSHS_high_hl_all_scores,paired=T) # there is difference between ll caps and hl caps p < 0.01
wilcox.exact(x=MSHS_high_ll_all_scores,y=MSHS_high_hh_all_scores,paired=T) # No difference
wilcox.exact(x=MSHS_high_lh_all_scores,y=MSHS_high_hl_all_scores,paired=T) # there is difference between lh caps and hl caps p < 0.01
wilcox.exact(x=MSHS_high_lh_all_scores,y=MSHS_high_hh_all_scores,paired=T) # No difference
wilcox.exact(x=MSHS_high_hl_all_scores,y=MSHS_high_hh_all_scores,paired=T) # There is difference between hl caps and hh caps p < 0.05


#----------------------------------------------------------------------------------------------------------




# SHQ high and MSHS high group ----------------------------------------------------------------------------
#SQH high and MSHS low

#SQHだけを設定して，SQHが高いほどユーモアへのスコアが高くなる

# MSHSを15以上,18以下, SQHを12以上にすると平均値が高いが MSHSを19い以下にすると平均値がだだ下がり
# ユーモアを適度に好む人はユーモアへの審査が厳しいと分かる

SQH_high_and_MSHS_high_group = subset(humor_scores, humor_scores$SQH_score >= 10 & humor_scores$MSHS_score <= 18 & humor_scores$MSHS_score >= 15)

par(mfrow=c(1,1))

SQH_high_and_MSHS_high_group_scores_mean = SQH_high_and_MSHS_high_group[6:10] / EXP_NUM
SQH_high_and_MSHS_high_group_mean = cbind(SQH_high_and_MSHS_high_group[1:5], SQH_high_and_MSHS_high_group_scores_mean)
summary(SQH_high_and_MSHS_high_group_mean[6:10])
boxplot(SQH_high_and_MSHS_high_group_mean[6:10], main="SQH high and SHSQ high group", names=c('baseline', 'LL caption', 'LH caption', 'HL caption', 'HH caption'), xlab="Captions", ylab="mean scores")

#SQH_high_and_MSHS_high_group_data = subset(data, data$SQH_score >= 10 & data$MSHS_score >= 12 & humor_scores$MSHS_score <= 17)
SQH_high_and_MSHS_high_group_data = subset(data, data$SQH_score >= 12 & humor_scores$MSHS_score <= 18)

SQH_HIGH_and_MSHS_HIGH_SUBJECT_NUM=length(SQH_high_and_MSHS_high_group[,1])

#each sim mean scores per subjects
SQH_high_and_MSHS_high_origin_caps = data.frame(SQH_high_and_MSHS_high_group_data[1:3])
SQH_high_and_MSHS_high_ll_caps = data.frame(SQH_high_and_MSHS_high_group_data[1:3])
SQH_high_and_MSHS_high_lh_caps = data.frame(SQH_high_and_MSHS_high_group_data[1:3])
SQH_high_and_MSHS_high_hl_caps = data.frame(SQH_high_and_MSHS_high_group_data[1:3])
SQH_high_and_MSHS_high_hh_caps = data.frame(SQH_high_and_MSHS_high_group_data[1:3])

for(i in 1:EXP_NUM){
  name = paste('exp1_q', i, '_origin', sep="")
  SQH_high_and_MSHS_high_origin_caps = data.frame(SQH_high_and_MSHS_high_origin_caps, SQH_high_and_MSHS_high_group_data[name])
  
  name = paste('exp1_q', i, '_ll', sep="")
  SQH_high_and_MSHS_high_ll_caps = data.frame(SQH_high_and_MSHS_high_ll_caps, SQH_high_and_MSHS_high_group_data[name])
  
  name = paste('exp1_q', i, '_lh', sep="")
  SQH_high_and_MSHS_high_lh_caps = data.frame(SQH_high_and_MSHS_high_lh_caps, SQH_high_and_MSHS_high_group_data[name])
  
  name = paste('exp1_q', i, '_hl', sep="")
  SQH_high_and_MSHS_high_hl_caps = data.frame(SQH_high_and_MSHS_high_hl_caps, SQH_high_and_MSHS_high_group_data[name])
  
  name = paste('exp1_q', i, '_hh', sep="")
  SQH_high_and_MSHS_high_hh_caps = data.frame(SQH_high_and_MSHS_high_hh_caps, SQH_high_and_MSHS_high_group_data[name])
}

# calculate frequency of each similarities
SQH_high_and_MSHS_high_origin_count = c()
SQH_high_and_MSHS_high_ll_count = c()
SQH_high_and_MSHS_high_lh_count = c()
SQH_high_and_MSHS_high_hl_count = c()
SQH_high_and_MSHS_high_hh_count = c()
for(i in 1:SQH_HIGH_and_MSHS_HIGH_SUBJECT_NUM){
  SQH_high_and_MSHS_high_origin_count = append(SQH_high_and_MSHS_high_origin_count, as.numeric(SQH_high_and_MSHS_high_origin_caps[i, 4:53]))
  SQH_high_and_MSHS_high_ll_count = append(SQH_high_and_MSHS_high_ll_count, as.numeric(SQH_high_and_MSHS_high_ll_caps[i, 4:53]))
  SQH_high_and_MSHS_high_lh_count = append(SQH_high_and_MSHS_high_lh_count, as.numeric(SQH_high_and_MSHS_high_lh_caps[i, 4:53]))
  SQH_high_and_MSHS_high_hl_count = append(SQH_high_and_MSHS_high_hl_count, as.numeric(SQH_high_and_MSHS_high_hl_caps[i, 4:53]))
  SQH_high_and_MSHS_high_hh_count = append(SQH_high_and_MSHS_high_hh_count, as.numeric(SQH_high_and_MSHS_high_hh_caps[i, 4:53]))
}
SQH_high_and_MSHS_high_origin_freq = table(SQH_high_and_MSHS_high_origin_count)
SQH_high_and_MSHS_high_ll_freq = table(SQH_high_and_MSHS_high_ll_count)
SQH_high_and_MSHS_high_lh_freq = table(SQH_high_and_MSHS_high_lh_count)
SQH_high_and_MSHS_high_hl_freq = table(SQH_high_and_MSHS_high_hl_count)
SQH_high_and_MSHS_high_hh_freq = table(SQH_high_and_MSHS_high_hh_count)


# create each freq barplot
par(mfrow=c(3,2))
barplot(SQH_high_and_MSHS_high_origin_freq, main="Baseline", xlab="Scores(Baseline)", ylab="Frequency", ylim=c(0,800))
barplot(SQH_high_and_MSHS_high_ll_freq, main="LL captions", xlab="Scores(LL Captions)", ylab="Frequency", ylim=c(0,800))
barplot(SQH_high_and_MSHS_high_lh_freq, main="LH captions", xlab="Scores(LH Captions)", ylab="Frequency", ylim=c(0,800))
barplot(SQH_high_and_MSHS_high_hl_freq, main="HL captions", xlab="Scores(Proposed method)", ylab="Frequency", ylim=c(0,800))
barplot(SQH_high_and_MSHS_high_hh_freq, main="HH captions", xlab="Scores(HH Captions)", ylab="Frequency", ylim=c(0,800))


#create list to collect each sims scores for all subjects.

SQH_high_and_MSHS_high_origin_all_scores = c()
SQH_high_and_MSHS_high_ll_all_scores = c()
SQH_high_and_MSHS_high_lh_all_scores = c()
SQH_high_and_MSHS_high_hl_all_scores = c()
SQH_high_and_MSHS_high_hh_all_scores = c()
for(i in 4:length(SQH_high_and_MSHS_high_origin_caps)){
  SQH_high_and_MSHS_high_origin_all_scores = c(SQH_high_and_MSHS_high_origin_all_scores, SQH_high_and_MSHS_high_origin_caps[,i])
  SQH_high_and_MSHS_high_ll_all_scores = c(SQH_high_and_MSHS_high_ll_all_scores, SQH_high_and_MSHS_high_ll_caps[,i])
  SQH_high_and_MSHS_high_lh_all_scores = c(SQH_high_and_MSHS_high_lh_all_scores, SQH_high_and_MSHS_high_lh_caps[,i])
  SQH_high_and_MSHS_high_hl_all_scores = c(SQH_high_and_MSHS_high_hl_all_scores, SQH_high_and_MSHS_high_hl_caps[,i])
  SQH_high_and_MSHS_high_hh_all_scores = c(SQH_high_and_MSHS_high_hh_all_scores, SQH_high_and_MSHS_high_hh_caps[,i])
}



# calculate wilcox.exact by above data
wilcox.exact(x=SQH_high_and_MSHS_high_origin_all_scores,y=SQH_high_and_MSHS_high_ll_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_high_and_MSHS_high_origin_all_scores,y=SQH_high_and_MSHS_high_lh_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_high_and_MSHS_high_origin_all_scores,y=SQH_high_and_MSHS_high_hl_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_high_and_MSHS_high_origin_all_scores,y=SQH_high_and_MSHS_high_hh_all_scores,paired=T)　# there is difference
wilcox.exact(x=SQH_high_and_MSHS_high_ll_all_scores,y=SQH_high_and_MSHS_high_lh_all_scores,paired=T) # No difference
wilcox.exact(x=SQH_high_and_MSHS_high_ll_all_scores,y=SQH_high_and_MSHS_high_hl_all_scores,paired=T) # there is difference between ll caps and hl caps p < 0.01
wilcox.exact(x=SQH_high_and_MSHS_high_ll_all_scores,y=SQH_high_and_MSHS_high_hh_all_scores,paired=T) # No difference
wilcox.exact(x=SQH_high_and_MSHS_high_lh_all_scores,y=SQH_high_and_MSHS_high_hl_all_scores,paired=T) # there is difference between lh caps and hl caps p < 0.01
wilcox.exact(x=SQH_high_and_MSHS_high_lh_all_scores,y=SQH_high_and_MSHS_high_hh_all_scores,paired=T) # No difference
wilcox.exact(x=SQH_high_and_MSHS_high_hl_all_scores,y=SQH_high_and_MSHS_high_hh_all_scores,paired=T) # There is difference between hl caps and hh caps p < 0.05











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

