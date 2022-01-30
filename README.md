# Blog-Api
This is a blog api that I made with Python. I use Django Rest Framework as a runtime and JWT for authentication/Authorization.
## Build and run
You can run the server with
`
docker-compose up --build -d
`
## Endpoints

### SignUp
-   method: `POST`
-   path: `/user/`
-   body: 
    ```js
    {
        "email": string,
        "password": string,
        "password2":string,
        "first_name":string,
        "last_name":string
    }
    ```
-   response:
    ```js
    {
    "id": integer,
    "first_name":string,
    "last_name": string,
    "email": string
    }
    ```

### Login
-   method: `POST`
-   path: `/user/login`
-   body: 
    ```js
    {
        "email": string,
        "password": string
    }
    ```
-   response:
    ```js
    {
    "status": boolean,
    "status code":integer,
    "token": string,
    }
    ```
### Post Create
-   method: `POST`
-   path: `/post/post/`
   * Header:
  
        |  Name | Description                           | Type   |
        |:---------:|---------------------------------------|--------|
        | Authorization | authentication token of the user  | String |
-   body: 
    ```js
    {
        "title": string,
        "content":string
    }
    ```
-   response:
    ```js
    {
    "id": integer,
    "title": string,
    "content": string,
    "user": integer,
    "favorited_by":array
    }
    ```
Method:"GET"-----Post List
Method:"DELETE"----Post Delete
### Add Favorite Post
-   method: `PUT`
-   path: `/post/favorite/:id/`
   * Header:
  
        |  Name | Description                           | Type   |
        |:---------:|---------------------------------------|--------|
        | Authorization | authentication token of the user  | String |
        
    ```
### Comment Create
-   method: `POST`
-   path: `/post/comment`
   * Header:
  
        |  Name | Description                           | Type   |
        |:---------:|---------------------------------------|--------|
        | Authorization | authentication token of the user  | String |
-   body: 
    ```js
{
    "post" : integer,
    "content" : string,
    "rating" : integer
}
    ```
-   response:
    ```js
    {
    "id": integer,
    "from": string,
    "to": string,
    "content":string,
    "createdAt": string
    }
    ```

