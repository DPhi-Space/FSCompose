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
url="127.0.0.1:5000"

docker compose up -d fsw gds

echo "Starting GDS GUI..."
for i in {5..1}; do
    echo "Time remaining: $i seconds"
    sleep 1
done

echo "Done!"

echo "Trying to open GDS GUI in browser..."
if command -v xdg-open > /dev/null; then
    xdg-open "$url"
elif command -v gnome-open > /dev/null; then
    gnome-open "$url"
elif command -v kde-open > /dev/null; then
    kde-open "$url"
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
        break
    fi
done

trap cleanup EXIT

