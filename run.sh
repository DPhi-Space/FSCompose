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
    sleep 0.02 # Optional: Add a small delay between lines
done

export CG_NETWORK="clustergate_network"
export GDS_PORT=5050

export ORIGINAL_DIR=$(pwd)


cleanup() {
    echo "Exiting script. Stopping FS..."
    docker stop fsw 
    sleep 2
    docker service rm gds pdb-api logger 
    sleep 2
    echo "Done Cleaning!"
}


set -e

./deploy/network.sh create 
./deploy/volume-creator.sh create
sleep 2
./deploy/registry.sh create
./deploy/logger.sh create
./deploy/fs.sh create
./deploy/apps.sh create
./deploy/apps.sh pdb_users


while true; do
    echo ""
    echo "######################################"
    echo ""
    echo "Setup done! Ready to fly."
    echo "Press 'q' to quit: "
    read q
    if [ "$q" = "q" ]; then
        set +e
        break
    fi
done

trap cleanup EXIT
