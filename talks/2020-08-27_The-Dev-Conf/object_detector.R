library(dplyr)
library(httr)

# Endpoint
endpoint <- 'http://max-object-detector.codait-prod-41208c73af8fca213512856c7a09db52-0000.us-east.containers.appdomain.cloud/'
# endpoint <- 'http://localhost:5000'  # if running docker locally or docker hub

object_detector <- function(path_to_img, endpoint) {
  model_endpoint <- paste0(endpoint, 'model/predict')  # Model endpoint
  # POST 
  response <- httr::POST(model_endpoint, 
                         body = list(image = upload_file(path_to_img, 
                                                         type = "image/jpeg")), 
                         encode = c("multipart")
  ) %>% content()
  response$predictions
}

object_detector("imgs/baby-bear.jpg", endpoint)
object_detector("imgs/dog-human.jpg", endpoint)
object_detector("imgs/jockey.jpg", endpoint)