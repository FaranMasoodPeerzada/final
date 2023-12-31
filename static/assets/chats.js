document.addEventListener("DOMContentLoaded", function () {
    // Get the conversation list elements
    const favouriteUsersList = document.getElementById("favourite-users");
    const usersList = document.getElementById("usersList");
    const chatMessages = document.querySelector("#users-conversation");

    let currentConversationId = null;

    function formatDateTime(timestamp) {
        const options = {
            year: 'numeric',
            month: 'numeric',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
           
        };
    
        return new Date(timestamp).toLocaleString('en-US', options);
    }
    // Function to handle the click event on a list item
    
    

    function handleListItemClick(idValue) {
        const parts = idValue.split("-");
        
        currentConversationId = parts[parts.length - 1];

        
        console.log("Clicked ID:", currentConversationId);
                
        fetch(`/get_chat_messages/${currentConversationId}/`)
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
                                            <p class="mb-0 ctext-content">Welcome to Leggo My Data!.</p>
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


            console.log("Updated ID:", currentConversationId);
            const messageForm = document.querySelector('.chatinput-form');
            const messageInput = document.querySelector('#chat-input');
            const messagesList = document.querySelector('.chat-conversation-list');

            messageForm.addEventListener('submit', (event) => {
                event.preventDefault();
            
                const message = messageInput.value.trim();
                
                if (message.length === 0) {
                  return;
                }
                sendUserMessage(currentConversationId, message);
                // messageInput.disabled = true;
              const timestamp = new Date().toLocaleTimeString('en-US', {
                  timeZone: 'Asia/Karachi',
                  year: 'numeric',
                  month: 'numeric',
                  day: 'numeric',
                  hour: 'numeric',
                  minute: 'numeric'
              });
            
                const messageItem = document.createElement('li');
                messageItem.classList.add('chat-list', 'right');
                messageItem.innerHTML = ` <div class="conversation-list">
                  <div class="user-chat-content">
                   <div class="ctext-wrap"> 
                    <div class="ctext-wrap-content">  
                     <p class="mb-0 ctext-content">${message}</p>    
                 </div>                            
                 <div class="dropdown align-self-start message-box-drop"> 
                  <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">  
                  <i class="ri-more-2-fill"></i>          
                  </a>                                
                  <div class="dropdown-menu">                                    
                  <a class="dropdown-item d-flex align-items-center justify-content-between reply-message" href="#" data-bs-toggle="collapse" data-bs-target=".replyCollapse">Reply 
                     <i class="bx bx-share ms-2 text-muted"></i>
                 </a>                                    
                 <a class="dropdown-item d-flex align-items-center justify-content-between" href="#" data-bs-toggle="modal" data-bs-target=".forwardModal">Forward 
                     <i class="bx bx-share-alt ms-2 text-muted"></i></a>           
                     <a class="dropdown-item d-flex align-items-center justify-content-between copy-message" href="#" id="copy-message-2">Copy 
                         <i class="bx bx-copy text-muted ms-2"></i></a>                                   
                          <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Bookmark
                              <i class="bx bx-bookmarks text-muted ms-2"></i></a>    
                               <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Mark as Unread 
                                 <i class="bx bx-message-error text-muted ms-2"></i></a>                         
                                 <a class="dropdown-item d-flex align-items-center justify-content-between delete-item" id="delete-item-2" href="#">Delete 
                                     <i class="bx bx-trash text-muted ms-2"></i></a>                            
                                 </div>                        
                             </div>                    
                         </div>                    
                         <div class="conversation-name">                        
                             <small class="text-muted time">${timestamp }</small>                        
                             <span class="text-warning check-message-icon"><i class="bx bx-check"></i>
                             </span>                    
                         </div>                
                     </div>            </div>       `;
                messagesList.appendChild(messageItem);
          
                messageInput.value = '';
            });

            function sendUserMessage(currentConversationId, message) {
                // Make an API request to OpenAI to get a response
                // You should replace 'YOUR_API_KEY' and 'YOUR_MODEL_ID' with your actual API key and model ID
               
                const formData = new FormData();
                formData.append('conversationId', currentConversationId);
                formData.append('message', message);

            fetch("/send_message/", {
             method: "POST",
            body: formData,
         })
        .then((response) => response.json())
                .then((data) => {
                    // Handle the response from OpenAI

                    const timestamp = new Date().toLocaleTimeString('en-US', {
                        timeZone: 'Asia/Karachi',
                        year: 'numeric',
                        month: 'numeric',
                        day: 'numeric',
                        hour: 'numeric',
                        minute: 'numeric'
                    });
                    const responseMessage = data.response; // Modify this based on the structure of the response
                    const messageItem = document.createElement('li');
                        messageItem.classList.add('chat-list', 'left');
                        messageItem.innerHTML = ` <div class="conversation-list">
                          <div class="user-chat-content">
                           <div class="ctext-wrap"> 
                            <div class="ctext-wrap-content">  
                             <p class="mb-0 ctext-content">${responseMessage}</p>    
                         </div>                            
                         <div class="dropdown align-self-start message-box-drop"> 
                          <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">  
                          <i class="ri-more-2-fill"></i>          
                          </a>                                
                          <div class="dropdown-menu">                                    
                          <a class="dropdown-item d-flex align-items-center justify-content-between reply-message" href="#" data-bs-toggle="collapse" data-bs-target=".replyCollapse">Reply 
                             <i class="bx bx-share ms-2 text-muted"></i>
                         </a>                                    
                         <a class="dropdown-item d-flex align-items-center justify-content-between" href="#" data-bs-toggle="modal" data-bs-target=".forwardModal">Forward 
                             <i class="bx bx-share-alt ms-2 text-muted"></i></a>           
                             <a class="dropdown-item d-flex align-items-center justify-content-between copy-message" href="#" id="copy-message-2">Copy 
                                 <i class="bx bx-copy text-muted ms-2"></i></a>                                   
                                  <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Bookmark
                                      <i class="bx bx-bookmarks text-muted ms-2"></i></a>    
                                       <a class="dropdown-item d-flex align-items-center justify-content-between" href="#">Mark as Unread 
                                         <i class="bx bx-message-error text-muted ms-2"></i></a>                         
                                         <a class="dropdown-item d-flex align-items-center justify-content-between delete-item" id="delete-item-2" href="#">Delete 
                                             <i class="bx bx-trash text-muted ms-2"></i></a>                            
                                         </div>                        
                                     </div>                    
                                 </div>                    
                                 <div class="conversation-name">                        
                                     <small class="text-muted time">${timestamp }</small>                        
                                     <span class="text-success check-message-icon"><i class="bx bx-check"></i>
                                     </span>                    
                                 </div>                
                             </div>            </div>      
                          `;
                          messagesList.appendChild(messageItem);
                      });
                }
        
        






            
    }
    
   // Function to create a message element based on your desired HTML structure
   function createMessageQuestionElement(message) {
    const messageElement = document.createElement("li");
    messageElement.classList.add("chat-list", "right");

    messageElement.innerHTML = `
        <div class="conversation-list">
            
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
                <small class="text-muted time">${formatDateTime(message.created_at)}</small>                        
                <span class="text-warning check-message-icon"><i class="bx bx-check"></i>
                </span>  
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
                LeggoData
                    <small class="text-muted mb-0 me-2">${formatDateTime(message.created_at)}</small>
                    <span class="me-1 text-success"><i class="bx bx-check-double bx-check"></i></span>
                </div>
            </div>
        </div>
    `;
    

    return messageElement;
}





  // Add a click event listener to each <li> element in favouriteUsersList
  const favouriteUserListItems = favouriteUsersList.querySelectorAll("li");
  favouriteUserListItems.forEach((liElement) => {
      liElement.addEventListener("click", function () {
          const idValue = this.getAttribute("id");
          handleListItemClick(idValue);
      });
  });

  // Add a click event listener to each <li> element in usersList
  const usersListItems = usersList.querySelectorAll("li");
  usersListItems.forEach((liElement) => {
      liElement.addEventListener("click", function () {
          const idValue = this.getAttribute("id");
          handleListItemClick(idValue);
      });
  });
  
});




