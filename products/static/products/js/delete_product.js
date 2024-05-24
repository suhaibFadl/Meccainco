$(document).ready(function () {  
    console.log("heeere") 
    const deleteButtons = document.querySelectorAll(".delete");
    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const objId = this.getAttribute("obj-id");
            console.log("obj-id:", objId);

            $.ajax({                
                url: delete_product_url,
                data: { 
                    "obj-id": objId,
                },
                success: function (response) {
                        $(`#delete-product-${objId}`).modal('hide')
                        $(".modal-backdrop").remove();
                        product_card = document.getElementById(`product-col-${objId}`)
                        product_card.remove();
                },
                error: function () {
                    console.error('Error performing search');
                }
            });

            // Perform any further actions based on objId and businessType
        });
    });
});