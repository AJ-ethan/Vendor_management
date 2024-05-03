# Vendor Management USING DJANGO REST FRAMEWORK 

### SETUP ###
    -  CREATE VIRTUAL ENVIROMENT USING - 
            python -m venv env
            activate virtualenv- Scripts/activate (for windows)
                                 source bin/activate(Linux)

    STEP2 - 
        CLONE FROM GITHUB OR DOWNLOAD ZIP
        - NAVIGATE TO BLOG APPLICATION USING TERMINAL
        - RUN COMMAND TO INSTALL REQUIREMENTS
                pip install -r requirements.txt

##           For Testing user can import POSTMAN Collection ##

### OR USER CAN DIRECTLY IMPORT Vendor Management.postman_collection.json in Postman ###
    
### RUN MIGRATIONS ###
    run command to migrate database
        - python manage.py migrate

### DETAILS AND API DESCRIPTIONS ###

    -- PROJECT CONTAIN ONE APP 
        "vendorProfile" - for Authentication and all APIs 
        

    -- Authentications is done using jwt token based authentications

## User Authentication and Register

    -- REGISTER:(POST REQUEST)
        http://127.0.0.1:8000/api/register/ 
    
    -- LOGIN:
        http://127.0.0.1:8000/api/login

        OUTPUT- IT GIVES TWO VALUES ONE IS ACCESS TOKEN AND ANOTHER IS REFERESH TOKEN
        // WITHOUT ACCESS TOKEN USER NOT ABLE TO ACCESS ANY API'S

    -- REFERESH : 

##  Data api's

    # FOR PUT AND POST REQUEST BODY FORMAT AND DATA PRESNAT IN JSON COLLECTION  

    1- VendorProfile GET and POST requests
        
        http://127.0.0.1:8000/api/vendors 

        GET Request output -- List of all vendors
        POST Request- 
                    Send this parameter in Body
                    {
                        "name":"name value",
                        "contract_details:"",
                        "address":"",
                        "vendor_code":"" // it must be unique
                    }


     #output contains details with likes and likes count
    
    2 - for update ,delete and getting specific Vendor detail api url-

        http://127.0.0.1:8000/api/vendors/<int:vendor_id>


    3.- PurchaseOrder GET and POST request

         http://127.0.0.1:8000/api/purchase_orders/

    4 - for update ,delete and getting specific "PurchaseOrder" api url

         http://127.0.0.1:8000/api/purchase_orders/<int:po_id>

    5 - Get Performance Matrics of specific Vendor

        http://127.0.0.1:8000/vendors/<int:vendor_id>/performance

        OUTPUT - returns four performance parameter

    6 - Achnowledgment api - user to take consideration of vendor for purchase order-POST

        http://127.0.0.1:8000/purchase_order/<int:po_id>/achnowledgment

    
    7 - History or log of vendor perfomance matrics- GET request only

        http://127.0.0.1:8000/vendor/performance/<int:vendor_id>/log








