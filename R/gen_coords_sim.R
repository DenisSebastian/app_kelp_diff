
library(sf)
coords <-  read.csv("data/csv/coords.csv")
coords_sf = st_as_sf(coords, coords = c("lon", "lat"), crs = 4326, agr = "constant") %>% 
    mutate(id = 1:nrow(.))

# library(mapview)
# mapview::mapview(coords_sf)
# 

alg <- zonas_urb_consolidadas %>% 
    filter(NOM_COMUNA == "ALGARROBO") 
    

out <- st_intersection(coords_sf, alg)
index <- out$id

coords_mar <- coords_sf[-index,] %>% 
    st_coordinates()

write.csv(coords_mar, "data/csv/coords_mar.csv")