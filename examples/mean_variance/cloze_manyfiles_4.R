



# -------------------------------


# Function to convert binary to decimal
binary_to_decimal <- function(binary_string) {
  # Split the binary string into individual digits
  digits <- as.integer(strsplit(as.character(binary_string), "")[[1]])
  
  
  # Calculate the decimal value
  decimal <- sum(digits * 2^((length(digits) - 1):0))
  
  return(as.character(decimal))
}



# Example usage
binary_num <- "101101"
decimal_num <- binary_to_decimal(binary_num)
print(paste("Binary:", binary_num, "Decimal:", decimal_num))




# -------------------------------



binary_to_hex <- function(binary_string) {
  # 1. Convert binary to decimal
  decimal_value <- strtoi(binary_string, base = 2)
  
  # 2. Convert decimal to hexadecimal
  hex_value <- toupper(as.character(as.hexmode(decimal_value)))
  
  return(hex_value)
}

# Example usage
binary_num1 <- "101101"
hex_num1 <- binary_to_hex(binary_num1)
print(paste("Binary:", binary_num1, "Hexadecimal:", hex_num1))

binary_num2 <- "11111111"
hex_num2 <- binary_to_hex(binary_num2)
print(paste("Binary:", binary_num2, "Hexadecimal:", hex_num2))

binary_num3 <- "10000000"
hex_num3 <- binary_to_hex(binary_num3)
print(paste("Binary:", binary_num3, "Hexadecimal:", hex_num3))

binary_num4 <- "0"
hex_num4 <- binary_to_hex(binary_num4)
print(paste("Binary:", binary_num4, "Hexadecimal:", hex_num4))

binary_num5 <- "1"
hex_num5 <- binary_to_hex(binary_num5)
print(paste("Binary:", binary_num5, "Hexadecimal:", hex_num5))

binary_num6 <- "1111111111111111"
hex_num6 <- binary_to_hex(binary_num6)
print(paste("Binary:", binary_num6, "Hexadecimal:", hex_num6))

#Alternative using a combination of string manipulation and hex conversion.
binary_to_hex_alt <- function(binary_string){
  decimal_val = strtoi(binary_string, base =2)
  hex_val = toupper(as.character(as.hexmode(decimal_val)))
  return(hex_val)
}

hex_num_alt1 = binary_to_hex_alt("101101")
print(paste("Binary: 101101, Hexadecimal:", hex))
            
            

# -------------------------------




decimal_to_hex <- function(decimal_str) {
  hex_value <- toupper(as.character(as.hexmode(strtoi(decimal_str, base = 10))))
  return(hex_value)
}

# Example usage
decimal_num1 <- "255"
hex_num1 <- decimal_to_hex(decimal_num1)
print(paste("Decimal:", decimal_num1, "Hexadecimal:", hex_num1))            




# -------------------------------



# Function to convert a decimal number to binary
decimal_to_binary <- function(decimal_num) {
  if (decimal_num == 0) {
    return("0")
  }
  
  binary_string <- ""
  num <- abs(decimal_num) # Handle negative numbers later
  
  while (num > 0) {
    remainder <- num %% 2
    binary_string <- paste0(remainder, binary_string)
    num <- floor(num / 2)
  }
  
  if(decimal_num < 0){
    # Handle negative numbers using two's complement.
    # First, find the binary representation of the absolute value.
    # Then, invert the bits and add 1.
    
    inverted_string <- gsub("0", "2", gsub("1", "0", binary_string))
    inverted_string <- gsub("2", "1", inverted_string)
    
    carry <- 1
    result_string <- ""
    for (i in nchar(inverted_string):1) {
      digit <- as.integer(substr(inverted_string, i, i))
      sum <- digit + carry
      result_string <- paste0(sum %% 2, result_string)
      carry <- floor(sum / 2)
    }
    
    if (carry == 1) {
      result_string <- paste0("1", result_string)
    }
    
    return(result_string)
    
  } else {
    return(binary_string)
  }
}

# Example usage
decimal_num <- 10
binary_num <- decimal_to_binary(decimal_num)
print(paste("Decimal:", decimal_num, "Binary:", binary_num))

decimal_num <- 0
binary_num <- decimal_to_binary(decimal_num)
print(paste("Decimal:", decimal_num, "Binary:", binary_num))

decimal_num <- 25
binary_num <- decimal_to_binary(decimal_num)
print(paste("Decimal:", decimal_num, "Binary:", binary_num))

decimal_num <- -10
binary_num <- decimal_to_binary(decimal_num)
print(paste("Decimal:", decimal_num, "Binary:", binary_num))

decimal_num <- -1
binary_num <- decimal_to_binary(decimal_num)
print(paste("Decimal:", decimal_num, "Binary:", binary_num))





# ------------------


decimal_to_binary <- function(n) {
  n <- as.numeric(n)

    if (n < 0) stop("Input must be a positive integer")
  if (n == 0) return("0")
  
  
  bits <- as.integer(rev(intToBits(n)))
  # Remove leading zeros
  binary_str <- paste(bits[which(bits == 1)[1]:length(bits)], collapse = "")
  return(binary_str)
}

# Example usage:
decimal_to_binary("10")  # Returns "1010"
decimal_to_binary("42")  # Returns "101010"
decimal_to_binary("34")  # Returns "101010"







decimal_to_binary <- function(n) {
  n <- as.numeric(n)
  
  if (n < 0) stop("Input must be a positive integer")
  if (n == 0) return("0")
  
  binary <- c()
  while (n > 0) {
    binary <- c(n %% 2, binary)
    n <- n %/% 2
  }
  return(paste(binary, collapse = ""))
}
decimal_to_binary("34")











