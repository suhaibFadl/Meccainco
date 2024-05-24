$(document).ready(function () {   
    const activationButtons = document.querySelectorAll(".activation");
    console.log('first', activationButtons)
    activationButtons.forEach(button => {
        button.addEventListener("click", function () {
            const objId = this.getAttribute("obj-id");
            const businessType = this.getAttribute("business-type");

            console.log("obj-id:", objId);
            console.log("business-type:", businessType);

            $.ajax({            
                url: "../ajax-activation",
                data: { 
                    "obj-id": objId,
                    "business-type": businessType
                },
                success: function (response) {
                    // Clear existing search results
                    if(businessType == 'store'){
                        $(`#de-activate-stores-${objId}`).modal('hide')
                        $(".modal-backdrop").remove();
                        store = document.getElementById(`store-col-${objId}`)
                        if(response.data){
                            store.innerHTML = `                                          
                            <button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#de-activate-stores-${objId}">
                                De-Activate
                            </button>`

                        }else{
                            store.innerHTML = `
                            <button type="button" obj-id=${objId} business-type="store" class="activation btn btn-primary">
                                Activate
                            </button>
                            `
                            console.log('2nd', activationButtons)
                        }
                    }
                    else if(businessType == 'workshop'){                
                        workshop = document.getElementById(`workshop-col-${objId}`)
                        $(`#de-activate-workshops-${objId}`).modal('hide')
                        $(".modal-backdrop").remove();
                        if(response.data){
                            workshop.innerHTML = `                                          
                            <button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#de-activate-workshops-${objId}">
                                De-Activate
                            </button>`
                        }else{
                            workshop.innerHTML = `                                                 
                            <button type="button" obj-id="${objId}" business-type="workshop" class="activation btn btn-primary">Activate</button>`
                        }
                    }
                },
                error: function () {
                    console.error('Error performing search');
                }
            });

            // Perform any further actions based on objId and businessType
        });
    });

    const deleteButtons = document.querySelectorAll(".delete");
    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const objId = this.getAttribute("obj-id");
            const businessType = this.getAttribute("business-type");

            console.log("obj-id:", objId);
            console.log("business-type:", businessType);

            $.ajax({                
                url: "../ajax-delete",
                data: { 
                    "obj-id": objId,
                    "business-type": businessType
                },
                success: function (response) {
                    if(businessType == 'store'){
                        $(`#de-delete-stores-${objId}`).modal('hide')
                        $(".modal-backdrop").remove();
                        store = document.getElementById(`store-row-${objId}`)
                        store.innerHTML = ``
                    }
                    else if(businessType == 'workshop'){
                        workshop = document.getElementById(`workshop-row-${objId}`)
                        $(`#de-activate-workshops-${objId}`).modal('hide')
                        $(".modal-backdrop").remove();
                        workshop = document.getElementById(`workshop-row-${objId}`)
                        workshop.innerHTML = ``
                        
                    }
                    else if(businessType == 'free'){
                        customer = document.getElementById(`customer-row-${objId}`)
                        $(`#delete-customers-${objId}`).modal('hide')
                        $(".modal-backdrop").remove();
                        customer = document.getElementById(`customer-row-${objId}`)
                        customer.innerHTML = ``
                        
                    }
                },
                error: function () {
                    console.error('Error performing search');
                }
            });

            // Perform any further actions based on objId and businessType
        });
    });
});
