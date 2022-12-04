


library(dplyr)
library(purrr)

path_csv <-  "data/csv"
names_areas <- list.files(path = path_csv, pattern = "Low*", full.names = F) %>%
    gsub(pattern = "Lowtide_KelpAreas_|_clean.csv", replacement = "",x = .)

    

csv_files <-  list.files(path = path_csv, pattern = "Low*", full.names = T) %>% 
    map(read.csv) %>% 
    map(~select(.,Image_date, area_kelp)) %>%
    set_names(names_areas) %>% 
    dplyr::bind_rows(.id = "variable") %>% 
    select(date = Image_date,Kelp = area_kelp, Site=variable)

head(csv_files)
write_csv2(csv_files, "data/csv/kelp_data.csv")

par <- read.csv("data/csv/PAR_data.csv") %>% 
    rename(date =date_start) %>% 
    select(-X)
write.csv(par, "data/csv/PAR_data.csv", row.names = FALSE)

SST <- read.csv("data/csv/SST_data.csv") %>% 
    rename(date =date_start) %>% 
    select(-X)
write.csv(SST, "data/csv/SST_data.csv", row.names = FALSE)


# names_files <- list.files(path = path_csv, pattern = "*data.csv", full.names = F) %>%
#     gsub(pattern = "_data.csv", replacement = "",x = .)
# 
# csv_files <-  list.files(path = path_csv, pattern = "data.csv*", full.names = T) %>% 
#     map(read.csv) %>% 
#     set_names(names_files) %>% 
#     dplyr::bind_rows(.id = "variable") %>% 
#     rename(date = date_start)
