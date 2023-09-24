document.addEventListener("DOMContentLoaded", function () {
    // Get the conversation list element
    const liElements = document.querySelectorAll("#favourite-users li, usersList li");
    const chatMessages = document.querySelector("#users-conversation");
  
    // Add a click event listener to the conversation list
   
// Add a click event listener to each <li> element
liElements.forEach((liElement) => {
    liElement.addEventListener("click", function () {
      // Get the value of the id attribute of the clicked <li> element
      const idValue = this.getAttribute("id");
      const parts = idValue.split("-");
      const conversationId = parts[parts.length - 1];
  
      console.log("Clicked ID:", conversationId);
      
      fetch(`/get_chat_messages/${conversationId}/`)
                  .then((response) => response.json())
                  .then((data) => {
                      chatMessages.innerHTML = ""; // Clear the "Loading..." message
  
                      if (data.messages.length === 0) {
                        // Define the HTML content to display when no messages are available
                        const noMessagesHTML = `
                          <li class="chast-list left">
                              <div class="conversation-list">
                                  <div class="user-chat-content">
                                      <div class="ctext-wrap"> 
                                          <div class="ctext-wrap-content">  
                                              <p class="mb-0 ctext-content">No messages available.</p>
                                          </div>
                                      </div>
                                  </div>
                              </div>
                          </li>
                        `;
                      
                        // Set the innerHTML of chatMessages to the noMessagesHTML
                        chatMessages.innerHTML = noMessagesHTML;
                        return;
                      }
  
                      // Display the chat messages
                      data.messages.forEach((message) => {
                          const messageElementquestion = createMessageQuestionElement(message);
                          chatMessages.appendChild(messageElementquestion);
                          const messageElementanswer = createMessageAnswerElement(message);
                          chatMessages.appendChild(messageElementanswer);
                      });
                  })
                  .catch((error) => {
                    console.error("Error fetching chat messages:", error);
                    chatMessages.innerHTML = "Failed to load messages.";
                });


      



      // You can now use the idValue as needed.
    });






   // Function to create a message element based on your desired HTML structure
   function createMessageQuestionElement(message) {
    const messageElement = document.createElement("li");
    messageElement.classList.add("chat-list", "right");

    messageElement.innerHTML = `
        <div class="conversation-list">
            <div class="chat-avatar">
                <div class="round-image">${message.question.charAt(0)}</div>
            </div>
            <div class="user-chat-content">
                <div class="ctext-wrap">
                    <div class="ctext-wrap-content">
                        <p class="mb-0 ctext-content">${message.question}</p>
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

function createMessageAnswerElement(message) {
    const messageElement = document.createElement("li");
    messageElement.classList.add("chat-list", "left");

    messageElement.innerHTML = `
        <div class="conversation-list">
            <div class="chat-avatar">
                <div class="round-image">${message.answer.charAt(0)}</div>
            </div>
            <div class="user-chat-content">
                <div class="ctext-wrap">
                    <div class="ctext-wrap-content">
                        <p class="mb-0 ctext-content">${message.answer}</p>
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
                    <small class="text-muted mb-0 me-2">${message.created_at}</small>LeggoData
                </div>
            </div>
        </div>
    `;
    

    return messageElement;
}








  });
  });
  