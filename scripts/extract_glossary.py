#!/usr/bin/env python3
"""
Extract glossary terms from multiple sources:
- Awesome Developer Dictionary
- ML Glossary
- MDN Web Docs Glossary
- CNCF Cloud Native Glossary
- Glosario (Carpentries)
Creates a comprehensive glossary.json with 1000+ tech terms
"""

import json
import re
import yaml
from pathlib import Path

def extract_awesome_dictionary(readme_path):
    """Extract terms from Awesome Developer Dictionary README"""
    terms = {}

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all term definitions (format: - **term**: definition)
    pattern = r'^- \*\*([^*]+)\*\*:\s*(.+?)(?=^- \*\*|\n\n|^##|\Z)'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

    for term, definition in matches:
        # Clean up the term and definition
        term = term.strip().lower()
        definition = definition.strip().replace('\n', ' ').replace('  ', ' ')

        # Remove markdown links but keep the text
        definition = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', definition)
        definition = re.sub(r'_see.*?_', '', definition).strip()

        if term and definition:
            terms[term] = {
                "term": term,
                "definition": definition,
                "category": categorize_term(term),
                "source": "Awesome Developer Dictionary"
            }

    return terms

def categorize_term(term):
    """Categorize a term based on common patterns"""
    term_lower = term.lower()

    # Categories based on keywords
    if any(x in term_lower for x in ['api', 'rest', 'graphql', 'soap', 'rpc']):
        return "API"
    elif any(x in term_lower for x in ['cloud', 'aws', 'azure', 'gcp', 'kubernetes', 'docker']):
        return "Cloud"
    elif any(x in term_lower for x in ['security', 'auth', 'encryption', 'ssl', 'https']):
        return "Security"
    elif any(x in term_lower for x in ['database', 'sql', 'nosql', 'redis', 'mongo']):
        return "Database"
    elif any(x in term_lower for x in ['javascript', 'python', 'java', 'c++', 'rust', 'go']):
        return "Programming Languages"
    elif any(x in term_lower for x in ['react', 'vue', 'angular', 'framework']):
        return "Frameworks"
    elif any(x in term_lower for x in ['git', 'version', 'svn', 'branch']):
        return "Version Control"
    elif any(x in term_lower for x in ['test', 'qa', 'unit', 'integration']):
        return "Testing"
    elif any(x in term_lower for x in ['agile', 'scrum', 'kanban', 'sprint']):
        return "Methodology"
    elif any(x in term_lower for x in ['ai', 'machine learning', 'ml', 'neural', 'deep learning']):
        return "AI/ML"
    elif any(x in term_lower for x in ['frontend', 'backend', 'full stack', 'ui', 'ux']):
        return "Web Development"
    elif any(x in term_lower for x in ['algorithm', 'data structure', 'complexity']):
        return "Computer Science"
    else:
        return "General"

def add_common_tech_terms():
    """Add additional common tech terms not in the dictionary"""
    additional_terms = {
        "react": {
            "term": "react",
            "definition": "A JavaScript library for building user interfaces, maintained by Facebook. React uses a component-based architecture and virtual DOM for efficient updates.",
            "category": "Frameworks",
            "source": "Common Knowledge"
        },
        "kubernetes": {
            "term": "kubernetes",
            "definition": "An open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications.",
            "category": "Cloud",
            "source": "Common Knowledge"
        },
        "docker": {
            "term": "docker",
            "definition": "A platform that uses OS-level virtualization to deliver software in packages called containers, which are isolated from one another and bundle their own software, libraries and configuration files.",
            "category": "Cloud",
            "source": "Common Knowledge"
        },
        "graphql": {
            "term": "graphql",
            "definition": "A query language for APIs and a runtime for executing those queries with your existing data, providing a complete and understandable description of the data in your API.",
            "category": "API",
            "source": "Common Knowledge"
        },
        "typescript": {
            "term": "typescript",
            "definition": "A strongly typed programming language that builds on JavaScript, giving you better tooling at any scale. TypeScript adds optional static typing and class-based object-oriented programming to JavaScript.",
            "category": "Programming Languages",
            "source": "Common Knowledge"
        },
        "webpack": {
            "term": "webpack",
            "definition": "A static module bundler for modern JavaScript applications that processes your application and creates a dependency graph of all modules your application needs.",
            "category": "Build Tools",
            "source": "Common Knowledge"
        },
        "nginx": {
            "term": "nginx",
            "definition": "A web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache. Known for its high performance, stability, rich feature set, simple configuration, and low resource consumption.",
            "category": "Infrastructure",
            "source": "Common Knowledge"
        },
        "redis": {
            "term": "redis",
            "definition": "An in-memory data structure store, used as a distributed, in-memory key-value database, cache, and message broker with optional durability.",
            "category": "Database",
            "source": "Common Knowledge"
        },
        "terraform": {
            "term": "terraform",
            "definition": "An infrastructure as code tool that lets you define both cloud and on-prem resources in human-readable configuration files that you can version, reuse, and share.",
            "category": "Cloud",
            "source": "Common Knowledge"
        },
        "prometheus": {
            "term": "prometheus",
            "definition": "An open-source systems monitoring and alerting toolkit that collects and stores metrics as time series data, with metrics information stored with the timestamp at which it was recorded.",
            "category": "Monitoring",
            "source": "Common Knowledge"
        }
    }

    # Add 100+ more essential terms
    more_terms = {
        "ansible": "An open-source software provisioning, configuration management, and application-deployment tool enabling infrastructure as code.",
        "jenkins": "An open-source automation server that enables developers to build, test, and deploy their software reliably.",
        "gitlab": "A web-based DevOps lifecycle tool that provides a Git repository manager with wiki, issue-tracking and CI/CD pipeline features.",
        "elasticsearch": "A distributed, RESTful search and analytics engine capable of addressing a growing number of use cases.",
        "kafka": "A distributed event streaming platform capable of handling trillions of events a day, used for high-performance data pipelines and streaming analytics.",
        "rabbitmq": "An open-source message-broker software that originally implemented the Advanced Message Queuing Protocol (AMQP).",
        "postgresql": "A powerful, open-source object-relational database system with over 30 years of active development.",
        "mongodb": "A source-available cross-platform document-oriented database program classified as a NoSQL database.",
        "cassandra": "A free and open-source, distributed, wide-column store, NoSQL database management system designed to handle large amounts of data.",
        "spark": "A unified analytics engine for large-scale data processing, providing high-level APIs in Java, Scala, Python and R.",
        "hadoop": "A framework that allows for the distributed processing of large data sets across clusters of computers using simple programming models.",
        "vue": "A progressive JavaScript framework for building user interfaces, designed to be incrementally adoptable.",
        "angular": "A TypeScript-based open-source web application framework led by the Angular Team at Google.",
        "svelte": "A free and open-source front end compiler that generates minimal and highly optimized JavaScript code from component files.",
        "nextjs": "A React framework that gives you building blocks to create web applications with server-side rendering and static website generation.",
        "nuxtjs": "An open-source framework built on top of Vue.js that makes web development simple and powerful.",
        "express": "A minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications.",
        "fastapi": "A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.",
        "django": "A high-level Python web framework that encourages rapid development and clean, pragmatic design.",
        "flask": "A micro web framework written in Python that doesn't require particular tools or libraries.",
        "spring": "An application framework and inversion of control container for the Java platform.",
        "laravel": "A free, open-source PHP web framework intended for the development of web applications following the MVC pattern.",
        "rails": "A server-side web application framework written in Ruby under the MIT License.",
        "golang": "An open source programming language that makes it easy to build simple, reliable, and efficient software.",
        "rust": "A multi-paradigm programming language designed for performance and safety, especially safe concurrency.",
        "swift": "A general-purpose, multi-paradigm, compiled programming language developed by Apple Inc.",
        "kotlin": "A cross-platform, statically typed, general-purpose programming language with type inference.",
        "scala": "A strong statically typed general-purpose programming language which supports both object-oriented and functional programming.",
        "elixir": "A dynamic, functional language designed for building maintainable and scalable applications that runs on the Erlang VM.",
        "haskell": "An advanced, purely functional programming language with strong static typing and lazy evaluation.",
        "clojure": "A dynamic, general-purpose programming language that combines the approachability of a scripting language with robust infrastructure.",
        "erlang": "A general-purpose, concurrent, functional programming language designed for building massively scalable soft real-time systems.",
        "lua": "A lightweight, high-level, multi-paradigm programming language designed primarily for embedded use in applications.",
        "perl": "A high-level, general-purpose, interpreted, dynamic programming language known for its text processing capabilities.",
        "php": "A popular general-purpose scripting language that is especially suited to web development.",
        "ruby": "A dynamic, open source programming language with a focus on simplicity and productivity.",
        "sass": "A preprocessor scripting language that is interpreted or compiled into CSS.",
        "less": "A backwards-compatible language extension for CSS that adds features like variables, mixins, and functions.",
        "tailwind": "A utility-first CSS framework packed with classes that can be composed to build any design directly in your markup.",
        "bootstrap": "A free and open-source CSS framework directed at responsive, mobile-first front-end web development.",
        "material-ui": "React components that implement Google's Material Design specification.",
        "jest": "A delightful JavaScript testing framework with a focus on simplicity that works with most JavaScript projects.",
        "mocha": "A feature-rich JavaScript test framework running on Node.js and in the browser.",
        "cypress": "A JavaScript end-to-end testing framework that makes testing anything running in a browser simple.",
        "selenium": "An umbrella project for various tools and libraries that enable web browser automation.",
        "playwright": "A framework for Web Testing and Automation that allows testing across all modern browsers.",
        "puppeteer": "A Node library which provides a high-level API to control headless Chrome or Chromium over the DevTools Protocol.",
        "postman": "An API platform for building and using APIs that simplifies each step of the API lifecycle.",
        "insomnia": "An open-source, cross-platform API client for GraphQL, REST, and gRPC.",
        "swagger": "A set of open-source tools built around the OpenAPI Specification that can help you design, build, document and consume REST APIs.",
        "openapi": "A specification for machine-readable interface files for describing, producing, consuming, and visualizing RESTful web services.",
        "grpc": "A modern open source high performance Remote Procedure Call (RPC) framework that can run in any environment.",
        "websocket": "A computer communications protocol providing full-duplex communication channels over a single TCP connection.",
        "oauth": "An open standard for access delegation commonly used as a way for Internet users to grant websites access to their information.",
        "jwt": "JSON Web Token is an open standard for securely transmitting information between parties as a JSON object.",
        "cors": "Cross-Origin Resource Sharing is a mechanism that allows restricted resources on a web page to be requested from another domain.",
        "csrf": "Cross-Site Request Forgery is an attack that forces an end user to execute unwanted actions on a web application.",
        "xss": "Cross-Site Scripting is a type of security vulnerability typically found in web applications.",
        "sql injection": "A code injection technique used to attack data-driven applications by inserting malicious SQL statements.",
        "https": "Hypertext Transfer Protocol Secure is an extension of HTTP that is used for secure communication over a computer network.",
        "ssl": "Secure Sockets Layer is a cryptographic protocol designed to provide communications security over a computer network.",
        "tls": "Transport Layer Security is a cryptographic protocol that provides end-to-end security of data sent between applications.",
        "ssh": "Secure Shell is a cryptographic network protocol for operating network services securely over an unsecured network.",
        "vpn": "Virtual Private Network extends a private network across a public network and enables users to send and receive data securely.",
        "firewall": "A network security system that monitors and controls incoming and outgoing network traffic based on security rules.",
        "load balancer": "A device that distributes network or application traffic across a number of servers to improve responsiveness and availability.",
        "cdn": "Content Delivery Network is a geographically distributed network of proxy servers that provide fast delivery of Internet content.",
        "dns": "Domain Name System is a hierarchical and decentralized naming system for computers connected to the Internet.",
        "tcp": "Transmission Control Protocol is one of the main protocols of the Internet protocol suite for reliable, ordered delivery of data.",
        "udp": "User Datagram Protocol is one of the core members of the Internet protocol suite used for low-latency and loss-tolerating connections.",
        "http": "Hypertext Transfer Protocol is an application protocol for distributed, collaborative, hypermedia information systems.",
        "rest": "Representational State Transfer is an architectural style for distributed hypermedia systems.",
        "soap": "Simple Object Access Protocol is a messaging protocol for exchanging structured information in web services.",
        "rpc": "Remote Procedure Call is a protocol that one program can use to request a service from a program on another computer.",
        "microservices": "An architectural style that structures an application as a collection of loosely coupled services.",
        "monolith": "A software application built as a single unified unit rather than a collection of loosely coupled services.",
        "serverless": "A cloud computing execution model where the cloud provider manages the infrastructure and automatically provisions resources.",
        "lambda": "AWS Lambda is an event-driven, serverless computing platform that runs code in response to events.",
        "ec2": "Amazon Elastic Compute Cloud provides scalable computing capacity in the AWS cloud.",
        "s3": "Amazon Simple Storage Service is an object storage service offering scalability, data availability, security, and performance.",
        "rds": "Amazon Relational Database Service is a distributed database service to set up, operate, and scale databases in the cloud.",
        "dynamodb": "Amazon DynamoDB is a fully managed proprietary NoSQL database service that supports key-value and document data structures.",
        "azure functions": "A serverless compute service that enables you to run event-triggered code without managing infrastructure.",
        "azure devops": "A set of development tools, services, and features to plan work, collaborate on code, and deploy applications.",
        "google cloud platform": "A suite of cloud computing services that runs on the same infrastructure that Google uses internally.",
        "firebase": "A platform developed by Google for creating mobile and web applications with real-time database and hosting.",
        "heroku": "A cloud platform as a service supporting several programming languages for deploying and running applications.",
        "netlify": "A San Francisco-based cloud computing company that offers hosting and serverless backend services for web applications.",
        "vercel": "A cloud platform for static sites and Serverless Functions that enables developers to host websites and web services.",
        "digitalocean": "An American cloud infrastructure provider that offers cloud services to help deploy and scale applications.",
        "linode": "An American cloud hosting company that provides virtual private servers and other cloud services.",
        "cloudflare": "A web infrastructure and website security company providing CDN services, DDoS mitigation, and distributed DNS.",
        "git": "A distributed version control system for tracking changes in source code during software development.",
        "github": "A provider of Internet hosting for software development and version control using Git.",
        "bitbucket": "A Git-based source code repository hosting service owned by Atlassian.",
        "svn": "Apache Subversion is a software versioning and revision control system distributed as open source.",
        "mercurial": "A distributed revision control tool for software developers that handles projects of any size.",
        "ci/cd": "Continuous Integration and Continuous Delivery/Deployment practices for automating software delivery.",
        "devops": "A set of practices that combines software development and IT operations to shorten the development lifecycle.",
        "sre": "Site Reliability Engineering is a discipline that incorporates aspects of software engineering applied to infrastructure.",
        "observability": "The ability to measure the internal states of a system by examining its outputs.",
        "monitoring": "The process of collecting, analyzing, and using information to track a program's progress and performance.",
        "logging": "The process of recording application events for debugging, auditing, and system monitoring.",
        "tracing": "A technique used to track the flow of a request through various services in a distributed system.",
        "metrics": "Numerical measurements recorded over time that track application and infrastructure performance.",
        "grafana": "An open-source platform for monitoring and observability that allows you to query, visualize, and alert on metrics.",
        "datadog": "A monitoring and analytics platform for cloud-scale applications, infrastructure, logs, and more.",
        "new relic": "A software analytics company that provides application performance management and monitoring.",
        "splunk": "A software platform to search, analyze and visualize machine-generated data gathered from websites and applications.",
        "elk stack": "Elasticsearch, Logstash, and Kibana - a collection of open-source tools for searching, analyzing, and visualizing data.",
        "machine learning": "A type of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
        "deep learning": "A subset of machine learning that uses neural networks with multiple layers to progressively extract higher-level features.",
        "neural network": "A series of algorithms that endeavors to recognize underlying relationships in data through a process that mimics the human brain.",
        "natural language processing": "A branch of AI that helps computers understand, interpret and manipulate human language.",
        "computer vision": "A field of AI that trains computers to interpret and understand the visual world.",
        "reinforcement learning": "An area of machine learning where an agent learns to make decisions by performing actions and receiving rewards.",
        "supervised learning": "A type of machine learning where the model is trained on labeled data.",
        "unsupervised learning": "A type of machine learning that looks for previously undetected patterns in data without pre-existing labels.",
        "tensorflow": "An open-source machine learning framework developed by Google for building and training neural networks.",
        "pytorch": "An open-source machine learning library based on the Torch library, used for computer vision and natural language processing.",
        "scikit-learn": "A free software machine learning library for Python featuring various classification, regression and clustering algorithms.",
        "keras": "An open-source software library that provides a Python interface for artificial neural networks.",
        "pandas": "A fast, powerful, flexible and easy to use open source data analysis and manipulation tool for Python.",
        "numpy": "A library for Python that adds support for large, multi-dimensional arrays and matrices with mathematical functions.",
        "jupyter": "An open-source web application that allows you to create and share documents containing live code, equations, and visualizations.",
        "anaconda": "A distribution of Python and R for scientific computing and data science.",
        "spacy": "An open-source library for advanced natural language processing in Python.",
        "nltk": "Natural Language Toolkit is a platform for building Python programs to work with human language data.",
        "opencv": "Open Source Computer Vision Library is a library of programming functions mainly aimed at real-time computer vision.",
        "blockchain": "A distributed ledger technology that maintains a continuously growing list of records, called blocks.",
        "cryptocurrency": "A digital or virtual currency secured by cryptography, making it nearly impossible to counterfeit.",
        "bitcoin": "A decentralized digital currency that can be sent from user to user on the peer-to-peer bitcoin network.",
        "ethereum": "A decentralized, open-source blockchain with smart contract functionality.",
        "smart contract": "Self-executing contracts with the terms of the agreement directly written into code.",
        "nft": "Non-Fungible Token is a unique digital identifier that cannot be copied, substituted, or subdivided.",
        "web3": "The idea of a new iteration of the World Wide Web incorporating concepts such as decentralization and blockchain.",
        "defi": "Decentralized Finance is a blockchain-based form of finance that does not rely on central financial intermediaries.",
        "dao": "Decentralized Autonomous Organization is an organization represented by rules encoded as a computer program.",
        "metaverse": "A collective virtual shared space created by the convergence of virtually enhanced physical and digital reality.",
        "ar": "Augmented Reality is an interactive experience that combines the real world and computer-generated content.",
        "vr": "Virtual Reality is a simulated experience that can be similar to or completely different from the real world.",
        "iot": "Internet of Things describes physical objects embedded with sensors and software for exchanging data over the internet.",
        "edge computing": "A distributed computing paradigm that brings computation and data storage closer to the sources of data.",
        "quantum computing": "A type of computation that harnesses quantum phenomena such as superposition and entanglement.",
        "5g": "The fifth generation technology standard for broadband cellular networks.",
        "big data": "Extremely large data sets that may be analyzed computationally to reveal patterns, trends, and associations.",
        "data science": "An interdisciplinary field that uses scientific methods to extract knowledge and insights from structured and unstructured data.",
        "data engineering": "The process of designing and building systems for collecting, storing, and analyzing data at scale.",
        "data warehouse": "A central repository of integrated data from one or more disparate sources for reporting and analysis.",
        "data lake": "A centralized repository that allows you to store all structured and unstructured data at any scale.",
        "etl": "Extract, Transform, Load is the process of copying data from one or more sources into a destination system.",
        "elt": "Extract, Load, Transform is a variant of ETL where data is loaded before transformation.",
        "data pipeline": "A series of data processing steps where the output of one step is the input of the next.",
        "stream processing": "The processing of data in motion, or in other words, computing on data directly as it is received.",
        "batch processing": "The processing of data in large blocks or batches rather than processing data streams in real-time.",
        "apache airflow": "An open-source workflow management platform for data engineering pipelines.",
        "apache beam": "A unified programming model for defining both batch and streaming data-parallel processing pipelines.",
        "apache flink": "A framework and distributed processing engine for stateful computations over unbounded and bounded data streams.",
        "dbt": "Data Build Tool is a command line tool that enables data analysts and engineers to transform data in their warehouse.",
        "snowflake": "A cloud computing-based data warehousing company that offers a cloud-based data storage and analytics service.",
        "databricks": "A unified analytics platform for big data and AI that provides a collaborative environment for data teams.",
        "tableau": "A visual analytics platform transforming the way we use data to solve problems.",
        "power bi": "A business analytics solution that lets you visualize your data and share insights across your organization.",
        "looker": "A business intelligence software and big data analytics platform that helps explore, analyze and share business analytics.",
        "metabase": "An open-source business intelligence tool that lets you ask questions about your data and displays answers in formats.",
        "superset": "An open-source data exploration and visualization platform designed to be visual, intuitive, and interactive.",
        "redash": "An open source tool that lets you connect and query your data sources, build dashboards and share them.",
        "business intelligence": "Technologies, applications and practices for the collection, integration, analysis, and presentation of business information.",
        "data visualization": "The graphical representation of information and data using visual elements like charts, graphs, and maps.",
        "dashboard": "A type of graphical user interface that displays key performance indicators and important data points.",
        "kpi": "Key Performance Indicator is a measurable value that demonstrates how effectively a company is achieving business objectives.",
        "sla": "Service Level Agreement is a commitment between a service provider and a client about particular aspects of the service.",
        "slo": "Service Level Objective is a key element of a service level agreement that describes measurable characteristics.",
        "sli": "Service Level Indicator is a carefully defined quantitative measure of some aspect of the level of service provided.",
        "okr": "Objectives and Key Results is a goal-setting framework for defining and tracking objectives and their outcomes.",
        "kpi dashboard": "A reporting tool that displays key performance indicators to help track progress toward business objectives.",
        "a/b testing": "A randomized experimentation process where two or more versions of a variable are shown to different user segments.",
        "feature flag": "A software development technique that turns functionality on and off without deploying new code.",
        "blue-green deployment": "A technique that reduces downtime by running two identical production environments called Blue and Green.",
        "canary deployment": "A technique to reduce risk when deploying new software by slowly rolling out changes to a small subset of users.",
        "rolling deployment": "A deployment strategy that slowly replaces previous versions of an application with new versions.",
        "infrastructure as code": "The process of managing and provisioning computer data centers through machine-readable definition files.",
        "configuration management": "A systems engineering process for establishing and maintaining consistency of a product's performance.",
        "orchestration": "The automated configuration, coordination, and management of computer systems and software.",
        "containerization": "A form of operating system virtualization where applications run in isolated user spaces called containers.",
        "virtualization": "The creation of a virtual version of something, such as a server, storage device, network or operating system.",
        "hypervisor": "Software that creates and runs virtual machines, allowing multiple operating systems to share hardware resources.",
        "bare metal": "A computer system without a base operating system or installed applications.",
        "cloud native": "An approach to building and running applications that exploits the advantages of the cloud computing delivery model.",
        "twelve-factor app": "A methodology for building software-as-a-service applications with best practices for portability and resilience.",
        "chaos engineering": "The discipline of experimenting on a system in order to build confidence in the system's capability to withstand turbulent conditions.",
        "resilience engineering": "A paradigm for safety management that focuses on how to help systems cope with complexity under pressure.",
        "fault tolerance": "The property that enables a system to continue operating properly in the event of failure of some components.",
        "high availability": "The ability of a system to operate continuously without failing for a designated period of time.",
        "disaster recovery": "A set of policies and procedures to enable the recovery of vital technology infrastructure after a disaster.",
        "backup": "The process of copying and archiving computer data so it may be used to restore the original after a data loss event.",
        "replication": "The process of copying data from one location to another to ensure consistency and improve reliability.",
        "sharding": "A database architecture pattern that separates large databases into smaller, faster, more manageable parts.",
        "partitioning": "The division of a logical database or its elements into distinct independent parts.",
        "indexing": "A data structure technique to efficiently retrieve records from database files based on some attributes.",
        "caching": "A technique to store copies of frequently accessed data in a cache to reduce access time.",
        "memoization": "An optimization technique that stores the results of expensive function calls and returns the cached result.",
        "lazy loading": "A design pattern that defers initialization of an object until the point at which it is needed.",
        "eager loading": "A design pattern where data is loaded immediately rather than when it is specifically requested.",
        "pagination": "The process of dividing a document or data set into discrete pages for viewing.",
        "throttling": "A technique to control the amount of incoming requests to a service to prevent overload.",
        "rate limiting": "A technique for limiting network traffic by restricting the number of requests a user can make in a given time.",
        "circuit breaker": "A design pattern used to detect failures and prevent cascading failures in distributed systems.",
        "retry logic": "A programming pattern that automatically retries failed operations with configurable policies.",
        "exponential backoff": "An algorithm that uses progressively longer waits between retries of failed operations.",
        "idempotency": "The property of operations that can be applied multiple times without changing the result beyond the initial application.",
        "eventual consistency": "A consistency model used in distributed computing that guarantees data convergence over time.",
        "strong consistency": "A consistency model where all reads return the most recent write for a given piece of data.",
        "acid": "Atomicity, Consistency, Isolation, Durability - a set of properties that guarantee database transactions are processed reliably.",
        "base": "Basically Available, Soft state, Eventual consistency - an alternative to ACID for distributed systems.",
        "cap theorem": "States that distributed systems can only guarantee two of: Consistency, Availability, and Partition tolerance.",
        "distributed system": "A system whose components are located on different networked computers that coordinate their actions.",
        "consensus algorithm": "A process used to achieve agreement on a single data value among distributed processes or systems.",
        "raft": "A consensus algorithm designed as an alternative to Paxos that is meant to be more understandable.",
        "paxos": "A family of protocols for solving consensus in a network of unreliable processors.",
        "byzantine fault tolerance": "The ability of a distributed system to reach consensus despite malicious actors in the system.",
        "two-phase commit": "A type of atomic commitment protocol for distributed systems that ensures all nodes commit or abort.",
        "saga pattern": "A design pattern for managing distributed transactions in microservices architectures.",
        "event sourcing": "A pattern where state changes are logged as a time-ordered sequence of records.",
        "cqrs": "Command Query Responsibility Segregation is a pattern that separates read and update operations for a data store.",
        "domain-driven design": "An approach to software development that centers the development on programming a domain model.",
        "hexagonal architecture": "An architectural pattern that aims to create loosely coupled application components.",
        "clean architecture": "A software design philosophy that separates the elements of a design into ring levels.",
        "mvc": "Model-View-Controller is a software design pattern commonly used for developing user interfaces.",
        "mvp": "Model-View-Presenter is a derivation of MVC architectural pattern used mostly for building user interfaces.",
        "mvvm": "Model-View-ViewModel is a software architectural pattern that facilitates separation of GUI development from business logic.",
        "singleton": "A software design pattern that restricts the instantiation of a class to one single instance.",
        "factory pattern": "A creational pattern that uses factory methods to deal with the problem of creating objects.",
        "observer pattern": "A software design pattern where an object maintains a list of dependents and notifies them of state changes.",
        "strategy pattern": "A behavioral design pattern that enables selecting an algorithm at runtime.",
        "decorator pattern": "A design pattern that allows behavior to be added to individual objects without affecting other objects.",
        "adapter pattern": "A software design pattern that allows the interface of an existing class to be used as another interface.",
        "facade pattern": "A software design pattern that provides a simplified interface to a library, framework, or complex set of classes.",
        "proxy pattern": "A software design pattern that provides a placeholder for another object to control access to it.",
        "dependency injection": "A technique whereby one object supplies the dependencies of another object.",
        "inversion of control": "A design principle in which custom-written portions of a program receive the flow of control from a framework.",
        "solid principles": "Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion principles.",
        "dry": "Don't Repeat Yourself is a principle aimed at reducing repetition of software patterns.",
        "kiss": "Keep It Simple, Stupid is a design principle that states most systems work best if they are kept simple.",
        "yagni": "You Aren't Gonna Need It is a principle that states a programmer should not add functionality until deemed necessary.",
        "law of demeter": "A design guideline for developing software that promotes loose coupling between objects.",
        "composition over inheritance": "A principle that classes should achieve polymorphic behavior through composition rather than inheritance.",
        "separation of concerns": "A design principle for separating a computer program into distinct sections.",
        "single source of truth": "The practice of structuring information models so that every data element is stored exactly once.",
        "convention over configuration": "A software design paradigm that attempts to decrease the number of decisions developers need to make.",
        "principle of least astonishment": "A principle that a component of a system should behave in a way that most users will expect.",
        "fail fast": "A principle that a system should report any failure condition as soon as it is detected.",
        "graceful degradation": "The ability of a system to maintain limited functionality even when parts of it are broken.",
        "progressive enhancement": "A strategy for web design that emphasizes core webpage content first, then adds layers of presentation.",
        "responsive design": "An approach to web design that makes web pages render well on a variety of devices and screen sizes.",
        "mobile-first": "A design strategy that starts with designing for mobile devices before designing for desktop.",
        "accessibility": "The design of products, devices, services, or environments for people with disabilities.",
        "internationalization": "The process of designing software so that it can be adapted to various languages and regions.",
        "localization": "The process of adapting internationalized software for a specific region or language.",
        "unicode": "A computing industry standard for consistent encoding, representation, and handling of text.",
        "utf-8": "A variable-width character encoding capable of encoding all valid code points in Unicode.",
        "ascii": "American Standard Code for Information Interchange is a character encoding standard for electronic communication.",
        "regex": "Regular Expression is a sequence of characters that define a search pattern for text processing.",
        "glob": "A pattern that specifies sets of filenames with wildcard characters.",
        "xpath": "A query language for selecting nodes or computing values from XML documents.",
        "json": "JavaScript Object Notation is a lightweight data-interchange format that is easy for humans to read and write.",
        "xml": "Extensible Markup Language is a markup language that defines rules for encoding documents.",
        "yaml": "YAML Ain't Markup Language is a human-readable data serialization language commonly used for configuration files.",
        "toml": "Tom's Obvious Minimal Language is a configuration file format that is easy to read due to obvious semantics.",
        "csv": "Comma-Separated Values is a delimited text file that uses commas to separate values.",
        "protocol buffers": "A language-neutral, platform-neutral extensible mechanism for serializing structured data.",
        "avro": "A row-oriented remote procedure call and data serialization framework developed within Apache's Hadoop project.",
        "parquet": "An open source, column-oriented data file format designed for efficient data storage and retrieval.",
        "orc": "Optimized Row Columnar is a columnar storage file format for Hadoop workloads.",
        "msgpack": "MessagePack is an efficient binary serialization format that is more compact than JSON.",
        "bson": "Binary JSON is a binary representation of JSON-like documents with extensions for additional data types.",
        "graphviz": "An open source graph visualization software that represents structural information as diagrams.",
        "plantuml": "An open-source tool allowing users to create UML diagrams from plain text descriptions.",
        "mermaid": "A JavaScript based diagramming and charting tool that renders Markdown-inspired text definitions.",
        "markdown": "A lightweight markup language for creating formatted text using a plain-text editor.",
        "restructuredtext": "A file format for textual data used primarily in Python documentation.",
        "asciidoc": "A text document format for writing notes, documentation, articles, books, and more.",
        "latex": "A document preparation system for high-quality typesetting often used for technical documentation.",
        "pandoc": "A universal document converter that can convert between numerous markup and word processing formats.",
        "sphinx": "A documentation generator written and used by the Python community.",
        "javadoc": "A documentation generator created by Sun Microsystems for the Java language.",
        "doxygen": "A documentation generator for multiple programming languages including C++, C, Java, and Python.",
        "swagger ui": "A collection of HTML, JavaScript, and CSS assets that dynamically generate documentation from a Swagger-compliant API.",
        "postman collections": "A group of saved requests organized into folders for API testing and documentation.",
        "api blueprint": "A documentation-oriented API description language for web APIs.",
        "raml": "RESTful API Modeling Language is a YAML-based language for describing RESTful APIs.",
        "asyncapi": "An open source initiative that provides a specification to define asynchronous APIs.",
        "openapi generator": "A tool to generate API client libraries, server stubs, and documentation from OpenAPI Specifications.",
        "json schema": "A vocabulary that allows you to annotate and validate JSON documents.",
        "protobuf": "Protocol Buffers are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data.",
        "thrift": "An interface definition language and binary communication protocol used for defining and creating services.",
        "avro schema": "A data serialization system that uses JSON for defining data types and protocols.",
        "graphql schema": "A type system that describes the capabilities of a GraphQL server and is used to validate queries.",
        "prisma": "An open-source database toolkit that makes database access easy with type safety and auto-completion.",
        "typeorm": "An ORM that can run in Node.js and can be used with TypeScript and JavaScript.",
        "sequelize": "A promise-based Node.js ORM for Postgres, MySQL, MariaDB, SQLite and Microsoft SQL Server.",
        "mongoose": "An Object Data Modeling (ODM) library for MongoDB and Node.js.",
        "sqlalchemy": "A SQL toolkit and Object-Relational Mapping (ORM) library for Python.",
        "hibernate": "An object-relational mapping tool for Java that provides a framework for mapping an object-oriented domain model.",
        "entity framework": "An open source object-relational mapper for ADO.NET developed by Microsoft.",
        "active record": "An architectural pattern found in software that stores in-memory object data in relational databases.",
        "data mapper": "A layer of software that separates the in-memory objects from the database.",
        "repository pattern": "A pattern that encapsulates the logic needed to access data sources.",
        "unit of work": "A pattern that maintains a list of objects affected by a business transaction and coordinates writing out changes.",
        "specification pattern": "A pattern whereby business rules can be recombined by chaining the business rules together.",
        "value object": "An immutable object that represents a descriptive aspect of the domain with no conceptual identity.",
        "aggregate": "A cluster of domain objects that can be treated as a single unit for data changes.",
        "bounded context": "A central pattern in Domain-Driven Design that defines boundaries within which a particular model is defined.",
        "ubiquitous language": "A language structured around the domain model and used by all team members.",
        "event storming": "A workshop-based method to quickly find out what is happening in the domain of a software program.",
        "user story": "An informal, natural language description of features of a software system written from an end-user perspective.",
        "acceptance criteria": "Conditions that a software product must meet to be accepted by a user, customer, or other stakeholder.",
        "definition of done": "A shared understanding of what it means for work to be complete.",
        "burndown chart": "A graphical representation of work left to do versus time in agile software development.",
        "velocity": "A metric used in agile software development to measure the amount of work a team can tackle during a sprint.",
        "story points": "A unit of measure for expressing an estimate of the overall effort required to implement a user story.",
        "planning poker": "A consensus-based, gamified technique for estimating effort or relative size of development goals.",
        "retrospective": "A meeting held by a project team at the end of a project or sprint to discuss what was successful and what could be improved.",
        "stand-up": "A daily meeting for the team to synchronize activities and create a plan for the next 24 hours.",
        "sprint": "A set period of time during which specific work has to be completed and made ready for review.",
        "backlog": "A prioritized list of features or technical work that the team maintains and works from.",
        "epic": "A large body of work that can be broken down into smaller user stories.",
        "spike": "A type of exploration story in agile software development aimed at answering questions or gathering information.",
        "technical debt": "The implied cost of additional rework caused by choosing an easy solution now instead of a better approach.",
        "refactoring": "The process of restructuring existing code without changing its external behavior.",
        "code review": "A software quality assurance activity in which one or more people check a program by viewing and reading its source code.",
        "pair programming": "An agile software development technique in which two programmers work together at one workstation.",
        "mob programming": "A software development approach where the whole team works on the same thing at the same time.",
        "trunk-based development": "A version control management practice where developers merge small, frequent updates to a core trunk.",
        "feature branch": "A branch created to work on a new feature that will eventually be merged back into the main branch.",
        "pull request": "A method of submitting contributions to a software project where changes are proposed and reviewed before merging.",
        "merge request": "GitLab's version of GitHub's Pull Request for proposing changes to a codebase.",
        "code coverage": "A measure used to describe the degree to which source code is executed when a test suite runs.",
        "cyclomatic complexity": "A software metric used to indicate the complexity of a program based on the number of linearly independent paths.",
        "static analysis": "The analysis of computer software performed without executing programs.",
        "dynamic analysis": "The testing and evaluation of a program by executing data in real-time.",
        "linting": "The process of running a program that analyzes code for potential errors.",
        "formatting": "The process of applying consistent style rules to source code for readability and maintainability.",
        "transpilation": "The process of converting source code from one programming language to another of similar abstraction level.",
        "compilation": "The process of converting source code into machine code or bytecode.",
        "interpretation": "The direct execution of source code by reading and executing it line by line.",
        "jit compilation": "Just-In-Time compilation is a way of executing code that involves compilation during execution of a program.",
        "aot compilation": "Ahead-Of-Time compilation is the act of compiling a program before it is executed.",
        "bytecode": "A form of instruction set designed for efficient execution by a software interpreter.",
        "machine code": "A set of instructions executed directly by a computer's central processing unit.",
        "assembly language": "A low-level programming language with a strong correspondence between the language and architecture's machine code.",
        "binary": "The compiled version of a program that can be directly executed by a computer.",
        "source code": "The human-readable instructions and statements written by a programmer using a programming language.",
        "open source": "Software with source code that anyone can inspect, modify, and enhance.",
        "proprietary software": "Software that is owned by an individual or a company and licensed under restrictive terms.",
        "freeware": "Software that is available free of charge but may have restrictions on use or distribution.",
        "shareware": "Software distributed on a trial basis with the understanding that users may need to pay for continued use.",
        "license": "A legal instrument governing the use or redistribution of software.",
        "mit license": "A permissive free software license that allows reuse with few restrictions.",
        "apache license": "A permissive free software license that requires preservation of copyright and disclaimer notices.",
        "gpl": "GNU General Public License is a copyleft license that requires derivative works to be open source.",
        "bsd license": "A family of permissive free software licenses with minimal restrictions on software redistribution.",
        "creative commons": "A set of free, public licenses that enable the distribution of copyrighted works.",
        "copyleft": "The practice of granting the right to freely distribute and modify a work with the requirement that the same rights be preserved.",
        "public domain": "Creative materials that are not protected by intellectual property laws and belong to the public.",
        "intellectual property": "Creations of the mind, such as inventions, literary works, designs, and symbols used in commerce.",
        "patent": "An exclusive right granted for an invention that provides a new way of doing something or offers a new technical solution.",
        "trademark": "A recognizable sign, design, or expression which identifies products or services of a particular source.",
        "copyright": "A legal right that grants the creator of original work exclusive rights to its use and distribution.",
        "trade secret": "A formula, practice, process, design, instrument, pattern, or compilation of information not generally known.",
        "nda": "Non-Disclosure Agreement is a legal contract between parties that outlines confidential material or knowledge.",
        "sla violation": "A breach of the agreed-upon service level commitments between a service provider and customer.",
        "incident": "An unplanned interruption to a service or reduction in the quality of a service.",
        "problem": "The cause of one or more incidents that requires investigation and resolution.",
        "change": "The addition, modification, or removal of anything that could have an effect on services.",
        "release": "A collection of hardware, software, documentation, processes or other components required to implement changes.",
        "rollback": "The process of reverting a system or application to a previous state after a failed deployment or change.",
        "hotfix": "A single, cumulative package that includes information used to address a problem in a software product.",
        "patch": "A piece of software designed to update a computer program or its supporting data to fix or improve it.",
        "upgrade": "The process of replacing a product with a newer version of the same product.",
        "downgrade": "The process of reverting software to an older version.",
        "migration": "The process of moving data, applications or other business elements from one environment to another.",
        "deprecation": "The discouragement of use of some feature, design, or practice, typically because it has been superseded.",
        "sunset": "The gradual phasing out and eventual termination of a product or service.",
        "eol": "End of Life is a term used to indicate that a product has reached the end of its useful life.",
        "legacy system": "An old method, technology, computer system, or application program that continues to be used.",
        "technical documentation": "Documentation that describes the architecture, components, and implementation of a technical system.",
        "api documentation": "Documentation that describes how to effectively use and integrate with an API.",
        "user documentation": "Documentation created for end users that explains how to use a software application.",
        "developer documentation": "Documentation aimed at developers that explains how to build, extend, or maintain software.",
        "system documentation": "Documentation that describes the system architecture, design, and implementation details.",
        "runbook": "A compilation of routine procedures and operations that system administrators or operators carry out.",
        "playbook": "A documented process or set of practices that a team follows to achieve a specific outcome.",
        "knowledge base": "A centralized repository for information that provides answers to common questions and solutions to problems.",
        "wiki": "A website or database developed collaboratively by a community of users, allowing any user to add and edit content.",
        "changelog": "A log or record of all notable changes made to a project, typically organized by version or release date.",
        "release notes": "Documentation that accompanies a software release and provides information about new features, improvements, and fixes.",
        "readme": "A text file that introduces and explains a project, containing information about installation, usage, and contribution.",
        "contributing guide": "Documentation that explains how to contribute to an open-source project.",
        "code of conduct": "A document that establishes expectations for behavior and participation in a project community.",
        "style guide": "A set of standards for writing and designing code to ensure consistency across a project.",
        "architecture decision record": "A document that captures an important architectural decision made along with its context and consequences.",
        "request for comments": "A document that proposes a change or addition to a system and solicits feedback from stakeholders.",
        "proof of concept": "A realization of a certain method or idea to demonstrate its feasibility.",
        "minimum viable product": "A version of a product with just enough features to satisfy early customers and provide feedback.",
        "prototype": "An early sample, model, or release of a product built to test a concept or process.",
        "wireframe": "A visual guide that represents the skeletal framework of a website or application.",
        "mockup": "A model or replica of a design used for teaching, demonstration, evaluation, or promotion.",
        "user interface": "The space where interactions between humans and machines occur.",
        "user experience": "A person's emotions and attitudes about using a particular product, system or service.",
        "information architecture": "The art and science of organizing and labeling content to support usability and findability.",
        "interaction design": "The practice of designing interactive digital products, environments, systems, and services.",
        "visual design": "The use of imagery, color, shapes, typography, and form to enhance usability and improve user experience.",
        "usability": "The ease of use and learnability of a human-made object such as a tool or device.",
        "affordance": "A property or feature of an object that indicates how it can be used.",
        "heuristic evaluation": "A usability inspection method for finding usability problems in a user interface design.",
        "user testing": "A technique used to evaluate a product or service by testing it with representative users.",
        "a/b test": "A randomized experiment with two variants, A and B, to determine which performs better.",
        "multivariate testing": "A technique for testing hypotheses on complex multi-variable systems.",
        "conversion rate": "The percentage of users who take a desired action on a website or application.",
        "bounce rate": "The percentage of visitors who navigate away from a site after viewing only one page.",
        "session": "A group of user interactions with a website that take place within a given time frame.",
        "pageview": "An instance of a page being loaded or reloaded in a browser.",
        "unique visitor": "A person who visits a website at least once within a given period.",
        "engagement": "The level of interaction and involvement a user has with a product or service.",
        "retention": "The ability of a product or service to keep users coming back over time.",
        "churn": "The rate at which customers stop doing business with an entity during a given time period.",
        "lifetime value": "A prediction of the net profit attributed to the entire future relationship with a customer.",
        "acquisition": "The process of gaining new users or customers for a product or service.",
        "activation": "The point at which a user first derives value from a product or service.",
        "referral": "When existing users recommend a product or service to others.",
        "revenue": "The income generated from normal business operations.",
        "monetization": "The process of converting something into a source of revenue.",
        "freemium": "A pricing strategy where a product or service is provided free of charge, but money is charged for additional features.",
        "subscription": "A business model where customers pay a recurring fee to access a product or service.",
        "saas": "Software as a Service is a software licensing and delivery model in which software is provided on a subscription basis.",
        "paas": "Platform as a Service is a cloud computing model that provides a platform for developing and deploying applications.",
        "iaas": "Infrastructure as a Service is a form of cloud computing that provides virtualized computing resources over the internet.",
        "baas": "Backend as a Service is a cloud service model that provides developers with ways to connect applications to backend cloud storage.",
        "faas": "Function as a Service is a cloud computing service that allows developers to run code in response to events without managing servers.",
        "caas": "Container as a Service is a cloud service model that allows users to upload, organize, run, scale, and manage containers.",
        "daas": "Desktop as a Service is a cloud computing offering where a service provider delivers virtual desktops to end users.",
        "dbaas": "Database as a Service is a cloud computing service that provides users with access to a database without setting up hardware.",
        "mbaas": "Mobile Backend as a Service is a model for providing web and mobile app developers with ways to link applications to backend cloud storage.",
        "naas": "Network as a Service is a business model for delivering network services virtually over the internet.",
        "seca": "Security as a Service is a business model in which a service provider integrates their security services into a corporate infrastructure.",
        "staas": "Storage as a Service is a business model in which a company leases or rents its storage infrastructure to another company.",
        "xaas": "Everything as a Service refers to the growing diversity of services available over the internet via cloud computing.",
        "on-premise": "Software that is installed and runs on computers on the premises of the organization using the software.",
        "hybrid cloud": "A cloud computing environment that uses a mix of on-premises, private cloud and public cloud services.",
        "multi-cloud": "The use of multiple cloud computing and storage services in a single heterogeneous architecture.",
        "vendor lock-in": "A situation in which a customer becomes dependent on a vendor for products and services.",
        "lift and shift": "A strategy for migrating an application or operation from one environment to another without redesign.",
        "rehost": "Moving applications to the cloud without making changes to optimize for the cloud.",
        "replatform": "Making a few cloud optimizations to achieve tangible benefits without changing the core architecture.",
        "repurchase": "Moving from a traditional license to a software-as-a-service model.",
        "refactor": "Re-imagining how an application is architected and developed using cloud-native features.",
        "retire": "Removing applications that are no longer needed.",
        "retain": "Keeping applications that are critical for the business but require major refactoring before migration.",
        "strangler pattern": "A method of gradually replacing a legacy system by incrementally replacing specific pieces of functionality.",
        "brownfield": "A software development project that involves modifying or expanding existing software systems.",
        "greenfield": "A software development project that lacks constraints imposed by prior work.",
        "proof of value": "A demonstration that a solution can deliver the expected business value.",
        "total cost of ownership": "The purchase price of an asset plus the costs of operation over its lifetime.",
        "return on investment": "A performance measure used to evaluate the efficiency or profitability of an investment.",
        "capital expenditure": "Funds used by a company to acquire, upgrade, and maintain physical assets.",
        "operating expenditure": "Ongoing costs for running a product, business, or system.",
        "time to market": "The length of time it takes from a product being conceived until it's available for sale.",
        "time to value": "The time it takes for a customer to realize value from a product after purchase.",
        "mean time to recovery": "The average time it takes to recover from a product or system failure.",
        "mean time between failures": "The average time between repairable failures of a technology product.",
        "mean time to failure": "The average time a non-repairable system or component is expected to operate before failing.",
        "availability": "The proportion of time a system is operational and accessible when required for use.",
        "reliability": "The probability that a system performs correctly during a specific duration.",
        "maintainability": "The ease with which a product can be maintained to correct defects, meet new requirements, or ensure continued operation.",
        "scalability": "The capability of a system to handle a growing amount of work or its potential to accommodate growth.",
        "elasticity": "The ability of a system to automatically provision and deprovision resources based on demand.",
        "performance": "The speed and efficiency with which a system or component accomplishes its designated functions.",
        "throughput": "The amount of data or number of operations that can be processed in a given time period.",
        "latency": "The time delay between a cause and an effect in a system.",
        "bandwidth": "The maximum rate of data transfer across a given path.",
        "qos": "Quality of Service is the description or measurement of the overall performance of a service.",
        "sre metrics": "Metrics used in Site Reliability Engineering to measure and maintain service reliability.",
        "error budget": "The maximum amount of time that a technical system can fail without contractual consequences.",
        "toil": "The kind of work tied to running a production service that tends to be manual, repetitive, and devoid of enduring value.",
        "runbook automation": "The ability to define, build, orchestrate, manage, and report on workflows that support system and network operational processes.",
        "chaos monkey": "A tool that randomly disables production instances to ensure that engineers implement resilient services.",
        "game day": "A practice where teams simulate failure scenarios to test system resilience and response procedures."
    }

    # Convert to proper format
    for term, definition in more_terms.items():
        additional_terms[term] = {
            "term": term,
            "definition": definition,
            "category": categorize_term(term),
            "source": "Common Knowledge"
        }

    return additional_terms

def extract_ml_glossary(glossary_path):
    """Extract terms from ML Glossary"""
    terms = {}

    with open(glossary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse RST format glossary entries
    # Format: .. _glossary_term:\n\nTerm Name\n\nDefinition...
    sections = content.split('.. _glossary_')

    for section in sections[1:]:  # Skip header
        lines = section.strip().split('\n')
        if len(lines) >= 3:
            # Extract term from anchor
            anchor = lines[0].split(':')[0].strip()
            # Find the term name (usually after a blank line)
            term_name = ''
            definition_lines = []
            found_term = False

            for i, line in enumerate(lines[1:]):
                if not found_term and line.strip() and not line.startswith('.'):
                    term_name = line.strip()
                    found_term = True
                elif found_term and line.strip() and not line.startswith('..'):
                    definition_lines.append(line.strip())

            if term_name and definition_lines:
                definition = ' '.join(definition_lines[:3])  # Take first 3 lines
                term_key = anchor.lower().replace('_', ' ')
                terms[term_key] = {
                    "term": term_key,
                    "definition": definition,
                    "category": "AI/ML",
                    "source": "ML Glossary"
                }

    return terms

def extract_mdn_glossary(mdn_dir):
    """Extract terms from MDN Web Docs glossary"""
    terms = {}
    glossary_path = Path(mdn_dir)

    if glossary_path.exists():
        for folder in glossary_path.iterdir():
            if folder.is_dir():
                index_file = folder / 'index.md'
                if index_file.exists():
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract title and definition from markdown
                    lines = content.split('\n')
                    title = folder.name.lower().replace('_', ' ').replace('-', ' ')

                    # Find the main definition (usually after the front matter)
                    definition = ''
                    in_front_matter = False
                    for line in lines:
                        if line.strip() == '---':
                            in_front_matter = not in_front_matter
                        elif not in_front_matter and line.strip() and not line.startswith('#'):
                            definition = line.strip()
                            break

                    if definition:
                        terms[title] = {
                            "term": title,
                            "definition": definition[:500],  # Limit length
                            "category": categorize_term(title),
                            "source": "MDN Web Docs"
                        }

    return terms

def extract_cncf_glossary(cncf_dir):
    """Extract terms from CNCF Cloud Native Glossary"""
    terms = {}
    glossary_path = Path(cncf_dir)

    if glossary_path.exists():
        for md_file in glossary_path.glob('*.md'):
            if md_file.name != '_index.md':
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract term and definition
                term = md_file.stem.replace('-', ' ').replace('_', ' ')

                # Find definition after front matter
                lines = content.split('\n')
                definition = ''
                in_front_matter = False
                for line in lines:
                    if line.strip() == '---':
                        in_front_matter = not in_front_matter
                    elif not in_front_matter and line.strip() and not line.startswith('#'):
                        definition = line.strip()
                        break

                if definition:
                    terms[term] = {
                        "term": term,
                        "definition": definition[:500],
                        "category": "Cloud Native",
                        "source": "CNCF Glossary"
                    }

    return terms

def extract_glosario(glosario_path):
    """Extract terms from Glosario multilingual glossary"""
    terms = {}

    try:
        with open(glosario_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        for entry in data:
            if 'en' in entry and 'slug' in entry:
                term = entry['slug'].replace('_', ' ').replace('-', ' ')
                if 'term' in entry['en']:
                    term = entry['en']['term']
                definition = entry['en'].get('def', '').strip()

                if term and definition:
                    terms[term.lower()] = {
                        "term": term.lower(),
                        "definition": definition[:500],
                        "category": categorize_term(term),
                        "source": "Glosario"
                    }
    except Exception as e:
        print(f"Error loading Glosario: {e}")

    return terms

def main():
    """Main function to create the glossary"""
    print("Extracting glossary terms from multiple sources...")
    glossary = {}

    # Extract from Awesome Developer Dictionary
    if Path("/tmp/awesome-developer-dictionary/README.md").exists():
        dict_terms = extract_awesome_dictionary("/tmp/awesome-developer-dictionary/README.md")
        glossary.update(dict_terms)
        print(f"✓ Awesome Developer Dictionary: {len(dict_terms)} terms")

    # Add common tech terms
    additional = add_common_tech_terms()
    glossary.update(additional)
    print(f"✓ Common Tech Terms: {len(additional)} terms")

    # Extract from ML Glossary
    if Path("/tmp/ml-glossary/docs/glossary.rst").exists():
        ml_terms = extract_ml_glossary("/tmp/ml-glossary/docs/glossary.rst")
        glossary.update(ml_terms)
        print(f"✓ ML Glossary: {len(ml_terms)} terms")

    # Extract from MDN Web Docs
    if Path("/tmp/content/files/en-us/glossary").exists():
        mdn_terms = extract_mdn_glossary("/tmp/content/files/en-us/glossary")
        # Only add unique terms
        for term, data in mdn_terms.items():
            if term not in glossary:
                glossary[term] = data
        print(f"✓ MDN Web Docs: {len(mdn_terms)} terms")

    # Extract from CNCF Glossary
    if Path("/tmp/glossary/content/en").exists():
        cncf_terms = extract_cncf_glossary("/tmp/glossary/content/en")
        for term, data in cncf_terms.items():
            if term not in glossary:
                glossary[term] = data
        print(f"✓ CNCF Glossary: {len(cncf_terms)} terms")

    # Extract from Glosario
    if Path("/tmp/glosario/glossary.yml").exists():
        glosario_terms = extract_glosario("/tmp/glosario/glossary.yml")
        for term, data in glosario_terms.items():
            if term not in glossary:
                glossary[term] = data
        print(f"✓ Glosario: {len(glosario_terms)} terms")

    print(f"\n📚 Total unique terms: {len(glossary)}")

    # Create output directory
    output_dir = Path("/home/jeremy/projects/blog/myblog/startaitools/static/data")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save as JSON
    output_file = output_dir / "glossary.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "terms": list(glossary.values()),
            "total": len(glossary),
            "categories": list(set(t["category"] for t in glossary.values())),
            "sources": list(set(t["source"] for t in glossary.values()))
        }, f, indent=2, ensure_ascii=False)

    print(f"\nGlossary saved to {output_file}")
    print(f"Categories: {', '.join(set(t['category'] for t in glossary.values()))}")

    # Print statistics
    categories = {}
    for term in glossary.values():
        cat = term["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\nTerms by category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} terms")

if __name__ == "__main__":
    main()