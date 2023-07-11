
 ## Following are the answers to the questions below: 

### How would you deploy this application in production?

Solution : 
To deploy this application in production, we can **containerize** the application, source.py using Docker. 
By containerizing the application, we can ensure consistent and reliable deployment across different environments.
The Docker container will encapsulate the application and its dependencies, making it easier to manage and deploy.
Moreover, we can improve security and flexibility by setting the credentials for the PostgreSQL database and SQS queue through environment variables. 
This approach allows us to securely store sensitive information separate from the application code and easily configure them based on the deployment environment.
By leveraging Docker and environment variables, we can streamline the deployment process and ensure the smooth operation of our application in production.


### What other components would you want to add to make this production ready?

Solution: 
To ensure the application is production-ready, it is crucial to establish a comprehensive **CI/CD pipeline** consisting of build, testing, and deployment phases.
By incorporating unit tests and integration tests during the testing phase, we can verify the application's functionality and stability before deployment.
The deployment process should be contingent upon the successful completion of the testing phase.
Implementing a CI/CD pipeline not only automates the build and deployment processes but also enhances code quality. 
It ensures that only thoroughly tested and validated code is pushed to the production environment, thereby reducing the risk of potential issues and ensuring a reliable application in production.
 

### How can this application scale with a growing dataset?

Solution:
To scale this application with a growing dataset, a recommended approach is to implement **load balancing** by creating multiple instances of the application and putting them behind a load balancer. 
This enables the distribution of incoming traffic across the instances, ensuring that the application can handle increased user demand and preventing it from becoming a bottleneck. 
By leveraging load balancing, the application can effectively scale with a growing dataset, accommodating multiple users and maintaining optimal performance.
Another approach is to use a **Kubernetes cluster**, which provides a scalable and flexible infrastructure for managing containerized applications.
With Kubernetes, the application can be dynamically scaled up or down based on demand, allowing it to handle larger datasets efficiently while ensuring high availability and resource optimization.


### How can PII be recovered later on?

Solution: 
To enable PII (Personally Identifiable Information) recovery, later on, there are a few strategies that can be implemented. 
- One approach is to **log the PII** being inserted into the database, either in a separate log file or in another column specifically designed to store the original PII.
- By preserving the original PII, it can be recovered when needed for legitimate purposes. Another method is to introduce original columns instead of directly selecting the PII during queries.
- This allows for the separation of sensitive information from publicly accessible data. 
- Additionally, database views can be created to expose only the necessary columns while masking sensitive information.
- For instance, functions like **SUBSTRING** can be used to partially mask email addresses, or the **REPLACE** function can be utilized to replace certain characters in a string. 
- By implementing these measures, PII can be protected while still allowing for its recovery when necessary.


### What are the assumptions you made?

Solution:

Here are the following assumptions which I have made:
- It can be observed that the "app_version" column's data is in the format "2.3.0" and has a datatype defined as "INT". So, I decided that the datatype should be changed from "INT" to **"VARCHAR"** to accommodate the app_version.
- The data being inserted into the database is **batched**, meaning that multiple records are inserted at once rather than being sent sequentially. This assumption is made based on the statement that it is better to insert data in a batch manner when dealing with large datasets.
- The last three digits of the "IP" address and the **last four digits** of the "device_id" are assumed to be **unique** in every case. Therefore, these specific digits have not been masked, likely to maintain the uniqueness and integrity of the data.
- These assumptions are made to provide context and make logical decisions based on the information provided.
