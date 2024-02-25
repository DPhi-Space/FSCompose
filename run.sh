#!/bin/bash

text="
                                                                                                             
                                                                                                             
   ######################         ##########################       #######             #######     ######    
   ########################       ###################                 ####             #######     ######    
   ##########################     #                                                       ####     ######    
                      #####                              ##########                                  ####    
                                      #########################    ####################                      
                            ###################################    ###########################     #         
                     ##########    ###########################     ###########################     ######    
                 #############    #########################        #######              ######     ######    
            #################     #######                          #######             #######     ######    
        ###################       #######                          #######             #######     ######    
     ###################          #######                          #######             #######     ######    
                                                                                                             
                                                                                                             
                                                                                                             
    ####                   ####                     ##                      ####                   ######    
   #    #                  #    #                  #  #                   ##    ##                           
    ####                   #   ##                 ##  ##                 ##                        ######    
        ##                 ####                   ######                  #     ##                           
   ######                  #                     ##    ##                  ######                  ######    
                                                                                                             
                                                                                                                                                                                                                                                                                                                                                                                      
                                                                                                                                                            
"

IFS=$'\n' # Set Internal Field Separator to newline
for line in $text; do
    echo "$line"
    sleep 0.05 # Optional: Add a small delay between lines
done
                                                                                                                                                                                                                             


cleanup() {
    echo "Exiting script. Stopping docker compose..."
    docker compose down
    echo "Done!"
}

docker compose pull fsw gds

docker compose -p clustergate up --force-recreate -d fsw gds

echo "Starting GDS GUI..."
for i in {5..1}; do
    echo "Time remaining: $i seconds"
    sleep 1
done

echo "Done!"

url="http://127.0.0.1:5000/"

echo "Trying to open GDS GUI in browser..."
if command -v xdg-open > /dev/null 2>&1; then
    xdg-open "$url" 2>/dev/null
elif command -v gnome-open > /dev/null 2>&1; then
    gnome-open "$url" 2>/dev/null
elif command -v kde-open > /dev/null 2>&1; then
    kde-open "$url" 2>/dev/null
else
    # Check if the terminal supports ANSI color codes
    if [ -t 1 ] && command -v tput &> /dev/null; then
        # ANSI color codes
        blue="$(tput setaf 4)"
        reset="$(tput sgr0)"

        # Display the URL in blue
        echo -e "Visit the following URL in your web browser:"
        echo -e "${blue}$url${reset}"
    else
        # If ANSI color codes are not supported, just display the URL without color
        echo "Visit the following URL in your web browser:"
        echo "$url"
    fi
fi


while true; do
    read -p "Press 'q' to quit: " q
    if [ "$q" = "q" ]; then
        docker compose down 
        docker stop clustergate-fsw-1
        docker stop clustergate-gds-1
        sleep 2
        docker network rm clustergate_my_network
        break
    fi
done

docker compose down 

trap cleanup EXIT
