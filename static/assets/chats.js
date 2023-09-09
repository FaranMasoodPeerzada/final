document.addEventListener("DOMContentLoaded", function () {
    const chatLinks = document.querySelectorAll(".list-unstyled");
    

    chatLinks.forEach(function (chatLink) {
        chatLink.addEventListener("click", function (event) {
            event.preventDefault();
            console.log("Clicked on conversation with ID:", 1);
            location.reload();
              // Clear previous messages
             
                  
        

            // Add your logic to handle the click event here.














        });





        // Function to create a message element based on your desired HTML structure
    function createMessageElement(message) {
        const messageElement = document.createElement("li");
        messageElement.classList.add("chat-list", "right");

        messageElement.innerHTML = `
            <div class="conversation-list">
                <div class="chat-avatar">
                    <div class="round-image">${message.user.charAt(0)}</div>
                </div>
                <div class="user-chat-content">
                    <div class="ctext-wrap">
                        <div class="ctext-wrap-content">
                            <p class="mb-0 ctext-content">${message.content}</p>
                        </div>
                        <div class="align-self-start message-box-drop dropdown">
                            <a role="button" aria-haspopup="true" class="btn btn-toggle" aria-expanded="false">
                                <i class="ri-more-2-fill"></i>
                            </a>
                            <div tabindex="-1" role="menu" aria-hidden="false" class="dropdown-menu show" data-popper-placement="top-start">
                                <button type="button" to="#" tabindex="0" role="menuitem" class="d-flex align-items-center justify-content-between dropdown-item">
                                    Copy <i class="bx bx-copy text-muted ms-2"></i>
                                </button>
                                <button type="button" to="#" tabindex="0" role="menuitem" class="d-flex align-items-center justify-content-between dropdown-item">
                                    Bookmark <i class="bx bx-bookmarks text-muted ms-2"></i>
                                </button>
                                <button type="button" tabindex="0" role="menuitem" class="d-flex align-items-center justify-content-between delete-item dropdown-item">
                                    Delete <i class="bx bx-trash text-muted ms-2"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="conversation-name">
                        <span class="me-1 text-success"><i class="bx bx-check-double bx-check"></i></span>
                        <small class="text-muted mb-0 me-2">${message.created_at}</small>You
                    </div>
                </div>
            </div>
        `;

        return messageElement;
    }
});

    });

