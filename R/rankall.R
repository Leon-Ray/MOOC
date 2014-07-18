rankall <- function(outcome, num = "best"){
  
  #read data 
  data <- read.csv("outcome-of-care-measures.csv", check.names = FALSE, stringsAsFactors = FALSE)
  
  #update data types for outcomes analyzed in assignment
  relevant_cols <- c(11,17,23)
  for (i in relevant_cols){
    data[, i] <- suppressWarnings(as.numeric(data[, i]))
  }
  
  #determine column index based on outcome argument 
  col_index <- match(tolower(paste("Hospital 30-Day Death (Mortality) Rates from", outcome)), tolower(names(data)))
  
  #per assignment instructions, stop if outcome argument is not one of three outcomes analyzed in assignment
  if (col_index %in% relevant_cols == FALSE){
    stop("invalid outcome")
  }

  #return hospital that matches the rank for that outcome, with hospital name as the tie breaker
  find_hospital <- function(data, col_index, num){
    small_df <- subset(data, data[, col_index] != "Not Available", select = c(2, col_index))
    len <- nrow(small_df)
    if (num == "worst"){
      num <- len
    }
    if (num == "best"){
      num <- 1
    }
    if (num > len){
      "<NA>"
    }
    sorted_df <- small_df[order(small_df[, 2], small_df[, 1]), ]
    sorted_df[num, 1]    
  }
  
  #split the dataset by state and apply find_hospital to each group
  hospital <- sapply(split(data, data$State), find_hospital, col_index = col_index, num = num )
  
  #additional processing for compatibility with autograder
  semi_final_df <- data.frame(hospital)
  final_df <- cbind(semi_final_df, row.names(semi_final_df))
  colnames(final_df)[2] <- "state"
  
  final_df
}