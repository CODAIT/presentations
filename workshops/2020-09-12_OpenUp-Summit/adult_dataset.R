### Load the library
library(aif360)
load_aif360_lib()

### Load the data 
original_data <- readr::read_csv(
  "https://www.dropbox.com/s/ga8tr1glji7nrgk/adult_data_preprocessed.csv?dl=1"
  )
original_data <- original_data[, -1]
head(original_data)
str(original_data)

# Predict whether income exceeds $50K/yr based on census data.
# Variables:
## sex: 1 male, 0 female
## income binary: 1 > 50k, 0 <= 50k

privileged_groups <- list('sex', 1)
unprivileged_groups <- list('sex', 0)

### 1) Convert the dataframe into the aif360 format ----------------------------
data_aif <- aif_dataset(data_path = original_data, 
                        favor_label = 1,         
                        unfavor_label = 0,       
                        privileged_protected_attribute = 1,
                        unprivileged_protected_attribute = 0,
                        target_column = "Income Binary", 
                        protected_attribute = "sex")

### 2) Let's  split in train and test ------------------------------------------
# train should be 70% 
# test should be 30% 
set.seed(1234)
data_aif_split <- data_aif$split(num_or_size_splits = list(0.70))
data_aif_train <- data_aif_split[[1]]
data_aif_test <- data_aif_split[[2]]


## 3) Calculate the mean  difference -------------------------------------------
metric_train <- binary_label_dataset_metric(data_aif_train, 
                                            privileged_groups = privileged_groups, 
                                            unprivileged_groups = unprivileged_groups)
metric_train$mean_difference()
# [1] -0.1932321
# The difference between the proportion of positive outcomes for the unprivileged vs
# the  privileged group
# P(𝑌=1|𝐷=unprivileged) −𝑃(𝑌=1|𝐷=privileged)



### 4) Apply adversarial debiasing -------------------------------------------
# (in-processing technique that learns a classifier to maximize prediction accuracy 
# and simultaneously reduce an adversary's ability to determine 
# the protected attribute from the predictions
sess <- tf$compat$v1$Session()

debiased_model <- adversarial_debiasing(privileged_groups = privileged_groups,
                                        unprivileged_groups = unprivileged_groups,
                                        scope_name = 'debiased_classifier',
                                        debias = TRUE,
                                        sess = sess)

debiased_model$fit(data_aif_train)
# predictions
data_aif_train_debiasing <- debiased_model$predict(data_aif_train)

# Right now we are just caring about fairness 
metric_preds <- binary_label_dataset_metric(data_aif_train_debiasing,
                                            privileged_groups = privileged_groups,
                                            unprivileged_groups = unprivileged_groups)

metric_preds$mean_difference()
# [1] -0.08583602 after
# [1] -0.1932321 before

