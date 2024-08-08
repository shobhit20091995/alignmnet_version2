# Combined Flask Application

This project merges two separate Flask applications into one, with different API endpoints for evaluating SMART criteria and analyzing similarity scores. The project uses transformers, NLTK, and sentence-transformers libraries.

## API Endpoints

1. **http://localhost:5000/evaluate_smat_criteria**: Evaluate Feasibility / SMART criteria.
2. **http://localhost:5000/analyze**: Analyze Similarity/Alignment scores.

## Requirements

- Docker
- Python 3.9

## Setup Instructions

1. **Build the Docker image:**

    ```sh
    docker build -t combined-app .
    ```

2. **Run the Docker container:**

    ```sh
    docker run -p 5000:5000 combined-app
    ```

## Endpoints Usage

### /evaluate_smat_criteria

**Request:**

- **Method:** POST
- **Content-Type:** application/json
- **Body:**
    ```json
{
  "artifactName":"ProjectCharter",
  "elements": {
  "Project Purpose or Justification": "UC Berkeley does not use energy as efficiently or as wisely as it could, leading to wastage. The project aims to emphasize individual actions through campus outreach to reduce campus and auxiliary energy usage, provide relevant information to stakeholders, and achieve a high participation rate.",
  "Objectives and Scope": "The project aims to develop, launch, and maintain a campus-wide campaign on energy reduction, accompanied by an incentive program for Operating Units. It includes the development of a campaign name, visual identity, website, marketing plan, competitions, energy audits, resources, communication with stakeholders, and coordination with the OE Procurement and IT teams.",
  "High-Level Requirements": "The project requires installation of proposed meters and related software at the beginning of the outreach campaign, demand for energy audits and resources to be met, finalization of decisions from procurement and IT teams affecting energy saving potential, and the buy-in and participation of Operating Units for estimated energy savings to be realized.",
  "Project Description": "The Marketing and Outreach project aims to address the inefficiency and wastage of energy at UC Berkeley by emphasizing individual actions through campus outreach and a campus-wide campaign on energy reduction.",
  "Deliverables": "Deliverables include the development and launch of the campus-wide campaign, creation of a website, energy usage records, visual identity, marketing materials, energy audits, and the roll-out of the campaign to all buildings.",
  "Success Criteria": {
    "1": "Reduced total campus and auxiliary energy usage",
    "2": "Relevant information provided to stakeholders",
    "3": "High Operating Unit participation rate"
  },
  "Start and End Dates": "Start date: Summer-Winter 2011; End date: On-going",
  "Key Dates and Milestones": {
    "Implementation team fully staffed": "July 2011; Summer-Winter 2011",
    "Formalized working relationship with Energy Office": "Summer 2011",
    "Marketing plan and materials developed": "By initial launch: Oct/Nov 2011",
    "Energy audits conducted (with Energy Office)": "Initial set of buildings: by initial launch (Oct/Nov 2011); on-going",
    "Initial launch": "Oct/Nov 2011",
    "Campaign rolled-out to all buildings": "Nov 2011 – on-going"
  },
  "Phases of Work": "Details may change upon the completion of the final workplan",
  "Constraints": "Constraints include assumptions on the implementation of the Energy Office and Incentive Program, potential greater demand for energy audits and resources than supply, finalization of decisions from procurement and IT teams, and the buy-in and participation of Operating Units.",
  "Assumptions": "Assumptions include the implementation of the Energy Office and Incentive Program, availability of resources for energy audits, timely finalization of decisions from procurement and IT teams, and the buy-in and participation of Operating Units.",
  "High-Level Project Risks": {
    "Risk": "Participation may be too low, program may be perceived as not fully successful, and financial savings may not be a sufficient motivator",
    "Mitigation Strategy": "Involvement of Operating Units, assessments and presentation of metrics, and an extensive marketing and outreach campaign"
  },
  "Budget Summary": "The project will require $510,000 in OE funding, with expected run-rate savings of $700,000.",
  "Stakeholder List": "Not available in the provided document",
  "Project Organization": "Not available in the provided document",
  "Approval Requirements": "The Project Sponsor signature indicates approval of the Project Charter",
  "Change Management Process": "Scope additions or changes will require a scope change request and formal approval by the Project Sponsor.",
  "Communication Plan": "Not available in the provided document"
}
}
### /analyze

**Request:**

- **Method:** POST
- **Content-Type:** application/json
- **Body:**
    ```json
{
  "artifacts": [
    {
      "artifactName": "Project",
      "Schedule": {
        "Master": {
          "Project Schedule": "Start Date: August 1, 2024 End Date: December 31, 2024 Phases of Work: Initiation, Planning, Execution, Closure Key Dates and Milestones: Project Kickoff, Requirement Gathering Completion, System Configuration Completion, User Training Completion, System Go-Live, Project Closure."
        },
        "Slaves": [
          {
            "Start and End Dates": "Start Date: August 1, 2024 End Date: December 31, 2024"
          },
          {
            "Phases of Work": "1. Initiation: Project kickoff, stakeholder identification, and requirement gathering. 2. Planning: Detailed project planning, resource allocation, and risk management. 3. Execution: System configuration, data migration, and user training. 4. Closure: System go-live, project evaluation, and closure activities."
          },
          {
            "Key Dates and Milestones": "1. Project Kickoff: August 1, 2024 2. Requirement Gathering Completion: August 31, 2024 3. System Configuration Completion: October 15, 2024 4. User Training Completion: November 30, 2024 5. System Go-Live: December 1, 2024 6. Project Closure: December 31, 2024"
          }
        ]
      },
      "Scope": {
        "Master": {
          "Project Scope": "Project Description: Deployment of a CRM system. Project Deliverables: Customized CRM system, integration interfaces, training materials. High-Level Requirements: Support for marketing, sales, and customer service functionalities. Objectives: Enhance customer satisfaction, increase sales efficiency. Scope Management: Defined scope inclusions and exclusions, scope control processes."
        },
        "Slaves": [
          {
            "Project Description": "This project involves the deployment of a comprehensive CRM system to manage customer interactions and sales processes. The scope includes the selection of a suitable CRM platform, customization to meet specific business needs, integration with existing systems, training for users, and ongoing support."
          },
          {
            "Project Deliverables": "1. Requirement Specification Document 2. Customized CRM System 3. Integration Interfaces with Existing Systems 4. Training Materials and Sessions 5. User Manuals and Documentation 6. Project Closure Report"
          },
          {
            "High-Level Requirements": "1. Implement a CRM system that supports marketing, sales, and customer service functionalities. 2. Integrate the CRM with existing enterprise systems. 3. Ensure the CRM provides real-time data analytics and reporting capabilities. 4. Facilitate user training and support to ensure smooth adoption. 5. Ensure data security and compliance with relevant regulations."
          },
          {
            "Objectives": "The primary objectives are to enhance customer satisfaction by providing personalized experiences, increase sales efficiency by automating sales processes, improve data accuracy and accessibility, and gain actionable insights through advanced analytics."
          },
          {
            "Scope Management": "Scope Definition: Implementation of a CRM system for marketing and sales. Scope Inclusions: System configuration, data migration, user training. Scope Exclusions: Post-implementation support, additional customizations beyond initial requirements. Scope Control: Regular scope reviews and change management processes to ensure deliverables are met."
          }
        ]
      },
      "Cost": {
        "Master": {
          "Project Cost": "Cost Management: Estimated total cost and financial plan. Resource Management: Human, financial, and material resources. Strategies for budget control and cost monitoring to ensure the project stays within budget."
        },
        "Slaves": [
          {
            "Cost Management": "Estimated Total Cost: $500,000. Financial Plan includes initial investment, operational costs, and contingency reserves. Budget control strategies include regular financial audits, cost monitoring through project management software, and contingency planning for unforeseen expenses."
          },
          {
            "Resource Management": "Resource Plan: Allocation of human, financial, and material resources. Human Resources: Project team members from IT, Marketing, and Sales. Financial Resources: Budget allocation for software, training, and support. Material Resources: Required technology and equipment. Procurement Management: Selection of CRM vendor and procurement of necessary licenses. Procurement Assessment: Regular evaluation of procurement processes to ensure efficiency and cost-effectiveness."
          }
        ]
      },
      "KPIs": {
        "Master": {
          "Project KPIs": "Performance Monitoring and Reporting: Key performance indicators to measure project success. Success Criteria: Criteria for evaluating project success, including user adoption rate, customer response time, sales efficiency, and data accuracy."
        },
        "Slaves": [
          {
            "Performance Monitoring and Reporting": "Key Performance Indicators (KPIs): Metrics include user adoption rate, customer response time, sales efficiency, and data accuracy. Monitoring and Reporting: Regular progress tracking and reporting to stakeholders through dashboards and status meetings."
          },
          {
            "Success Criteria": "1. User Adoption Rate of 90% within the first three months 2. Reduction in Customer Response Time by 30% 3. Increase in Sales Efficiency by 25% 4. Data Accuracy Improvement by 20% 5. Compliance with all relevant data security regulations"
          }
        ]
      }
    },
    {
      "artifactName": "Business",
      "Goals": {
        "Master": {
          "Business Goals": "The project's goals are aligned with the business's vision, mission, and strategic objectives. The CRM system implementation aims to enhance customer satisfaction, increase sales efficiency, and provide valuable business insights, contributing to overall business growth and success."
        },
        "Slaves": [
          {
            "Project Purpose": "The CRM Implementation project aims to enhance the company's ability to manage customer interactions and sales processes efficiently. This necessity arises from the need to address business needs for improved customer engagement, meet market demand for streamlined sales operations, respond to customer requests for better service, leverage technological advancements in CRM systems, comply with legal requirements for data management, and fulfill social needs for personalized customer experiences."
          },
          {
            "Business Outcomes": "Strategic Alignment: CRM system aligns with the company's strategic objectives for customer engagement and sales growth. Economic Impact: Projected financial benefits include revenue growth and cost savings. Operational Improvements: Improved operational efficiency and data-driven decision-making. Market Position: Enhanced competitive advantage through better customer relationship management."
          }
        ]
      },
      "Objectives": {
        "Master": {
          "Business Objectives": "The project objectives include successful CRM system deployment, high user adoption rate, improved customer engagement, and increased sales efficiency. These objectives support the business's strategic goals and long-term vision."
        },
        "Slaves": [
          {
            "Objectives": "The primary objectives are to enhance customer satisfaction by providing personalized experiences, increase sales efficiency by automating sales processes, improve data accuracy and accessibility, and gain actionable insights through advanced analytics. These objectives align with stakeholder expectations for better customer relationship management and improved sales performance."
          }
        ]
      },
      "Strategy": {
        "Master": {
          "Business Strategy": "The project strategy focuses on leveraging the CRM system to gain a competitive edge, enhance customer relationships, and streamline sales processes. It includes detailed market analysis, competitor analysis, and well-defined sales and marketing strategies."
        },
        "Slaves": [
          {
            "Methodology Selection": "The project will employ a Hybrid methodology, combining Waterfall for the initial planning and design phases, and Agile for the execution and implementation phases. This approach ensures detailed upfront planning and flexibility during execution, aligning with the project goals and constraints."
          }
        ]
      },
      "KPIs": {
        "Master": {
          "Business KPI": "Key performance indicators for the project include user adoption rate, customer response time, sales efficiency, and data accuracy. These KPIs will be monitored and reported regularly to measure the project's success and alignment with business goals."
        },
        "Slaves": [
          {
            "Performance Monitoring and Reporting": "Key Performance Indicators (KPIs): Metrics include user adoption rate, customer response time, sales efficiency, and data accuracy. Monitoring and Reporting: Regular progress tracking and reporting to stakeholders through dashboards and status meetings."
          },
          {
            "Success Criteria": "1. User Adoption Rate of 90% within the first three months 2. Reduction in Customer Response Time by 30% 3. Increase in Sales Efficiency by 25% 4. Data Accuracy Improvement by 20% 5. Compliance with all relevant data security regulations"
          }
        ]
      }
    }
  ]
}
## Dependencies

All dependencies are listed in the `requirements.txt` file. The main dependencies are:

- Flask==2.3.2
- nltk
- sentence-transformers
- pandas
- transformers==4.29.2
- torch==2.0.1
- numpy<2

## Notes

- Ensure Docker is installed and running on your system.
- The application will be available at `http://localhost:5000` after running the Docker container.
