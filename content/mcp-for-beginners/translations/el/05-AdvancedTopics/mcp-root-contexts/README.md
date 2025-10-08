<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "ebdb86db46113f1cbd59ce4c74caaa79",
  "translation_date": "2025-07-17T05:42:43+00:00",
  "source_file": "05-AdvancedTopics/mcp-root-contexts/README.md",
  "language_code": "el"
}
-->
# MCP Root Contexts

Οι root contexts είναι μια βασική έννοια στο Model Context Protocol που παρέχει ένα μόνιμο επίπεδο για τη διατήρηση του ιστορικού συνομιλίας και της κοινής κατάστασης σε πολλαπλά αιτήματα και συνεδρίες.

## Εισαγωγή

Σε αυτό το μάθημα, θα εξερευνήσουμε πώς να δημιουργούμε, να διαχειριζόμαστε και να χρησιμοποιούμε root contexts στο MCP.

## Στόχοι Μάθησης

Στο τέλος αυτού του μαθήματος, θα μπορείτε να:

- Κατανοείτε τον σκοπό και τη δομή των root contexts
- Δημιουργείτε και να διαχειρίζεστε root contexts χρησιμοποιώντας τις βιβλιοθήκες πελάτη MCP
- Υλοποιείτε root contexts σε εφαρμογές .NET, Java, JavaScript και Python
- Χρησιμοποιείτε root contexts για συνομιλίες πολλαπλών βημάτων και διαχείριση κατάστασης
- Εφαρμόζετε βέλτιστες πρακτικές για τη διαχείριση root contexts

## Κατανόηση των Root Contexts

Τα root contexts λειτουργούν ως δοχεία που κρατούν το ιστορικό και την κατάσταση για μια σειρά σχετικών αλληλεπιδράσεων. Επιτρέπουν:

- **Διατήρηση Συνομιλίας**: Διατήρηση συνεκτικών συνομιλιών πολλαπλών βημάτων
- **Διαχείριση Μνήμης**: Αποθήκευση και ανάκτηση πληροφοριών μεταξύ αλληλεπιδράσεων
- **Διαχείριση Κατάστασης**: Παρακολούθηση προόδου σε πολύπλοκες ροές εργασίας
- **Κοινή Χρήση Πλαισίου**: Επιτρέπουν σε πολλούς πελάτες να έχουν πρόσβαση στην ίδια κατάσταση συνομιλίας

Στο MCP, τα root contexts έχουν τα εξής βασικά χαρακτηριστικά:

- Κάθε root context έχει ένα μοναδικό αναγνωριστικό.
- Μπορούν να περιέχουν ιστορικό συνομιλίας, προτιμήσεις χρήστη και άλλα μεταδεδομένα.
- Μπορούν να δημιουργηθούν, να προσπελαστούν και να αρχειοθετηθούν ανάλογα με τις ανάγκες.
- Υποστηρίζουν λεπτομερή έλεγχο πρόσβασης και δικαιώματα.

## Κύκλος Ζωής Root Context

```mermaid
flowchart TD
    A[Create Root Context] --> B[Initialize with Metadata]
    B --> C[Send Requests with Context ID]
    C --> D[Update Context with Results]
    D --> C
    D --> E[Archive Context When Complete]
```

## Εργασία με Root Contexts

Ακολουθεί ένα παράδειγμα για το πώς να δημιουργήσετε και να διαχειριστείτε root contexts.

### Υλοποίηση σε C#

```csharp
// .NET Example: Root Context Management
using Microsoft.Mcp.Client;
using System;
using System.Threading.Tasks;
using System.Collections.Generic;

public class RootContextExample
{
    private readonly IMcpClient _client;
    private readonly IRootContextManager _contextManager;
    
    public RootContextExample(IMcpClient client, IRootContextManager contextManager)
    {
        _client = client;
        _contextManager = contextManager;
    }
    
    public async Task DemonstrateRootContextAsync()
    {
        // 1. Create a new root context
        var contextResult = await _contextManager.CreateRootContextAsync(new RootContextCreateOptions
        {
            Name = "Customer Support Session",
            Metadata = new Dictionary<string, string>
            {
                ["CustomerName"] = "Acme Corporation",
                ["PriorityLevel"] = "High",
                ["Domain"] = "Cloud Services"
            }
        });
        
        string contextId = contextResult.ContextId;
        Console.WriteLine($"Created root context with ID: {contextId}");
        
        // 2. First interaction using the context
        var response1 = await _client.SendPromptAsync(
            "I'm having issues scaling my web service deployment in the cloud.", 
            new SendPromptOptions { RootContextId = contextId }
        );
        
        Console.WriteLine($"First response: {response1.GeneratedText}");
        
        // Second interaction - the model will have access to the previous conversation
        var response2 = await _client.SendPromptAsync(
            "Yes, we're using containerized deployments with Kubernetes.", 
            new SendPromptOptions { RootContextId = contextId }
        );
        
        Console.WriteLine($"Second response: {response2.GeneratedText}");
        
        // 3. Add metadata to the context based on conversation
        await _contextManager.UpdateContextMetadataAsync(contextId, new Dictionary<string, string>
        {
            ["TechnicalEnvironment"] = "Kubernetes",
            ["IssueType"] = "Scaling"
        });
        
        // 4. Get context information
        var contextInfo = await _contextManager.GetRootContextInfoAsync(contextId);
        
        Console.WriteLine("Context Information:");
        Console.WriteLine($"- Name: {contextInfo.Name}");
        Console.WriteLine($"- Created: {contextInfo.CreatedAt}");
        Console.WriteLine($"- Messages: {contextInfo.MessageCount}");
        
        // 5. When the conversation is complete, archive the context
        await _contextManager.ArchiveRootContextAsync(contextId);
        Console.WriteLine($"Archived context {contextId}");
    }
}
```

Στον παραπάνω κώδικα έχουμε:

1. Δημιουργήσει ένα root context για μια συνεδρία υποστήριξης πελατών.
1. Στείλει πολλαπλά μηνύματα μέσα σε αυτό το context, επιτρέποντας στο μοντέλο να διατηρεί την κατάσταση.
1. Ενημερώσει το context με σχετικά μεταδεδομένα βάσει της συνομιλίας.
1. Ανακτήσει πληροφορίες του context για να κατανοήσει το ιστορικό της συνομιλίας.
1. Αρχειοθετήσει το context όταν η συνομιλία ολοκληρώθηκε.

## Παράδειγμα: Υλοποίηση Root Context για χρηματοοικονομική ανάλυση

Σε αυτό το παράδειγμα, θα δημιουργήσουμε ένα root context για μια συνεδρία χρηματοοικονομικής ανάλυσης, δείχνοντας πώς να διατηρείται η κατάσταση σε πολλαπλές αλληλεπιδράσεις.

### Υλοποίηση σε Java

```java
// Java Example: Root Context Implementation
package com.example.mcp.contexts;

import com.mcp.client.McpClient;
import com.mcp.client.ContextManager;
import com.mcp.models.RootContext;
import com.mcp.models.McpResponse;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class RootContextsDemo {
    private final McpClient client;
    private final ContextManager contextManager;
    
    public RootContextsDemo(String serverUrl) {
        this.client = new McpClient.Builder()
            .setServerUrl(serverUrl)
            .build();
            
        this.contextManager = new ContextManager(client);
    }
    
    public void demonstrateRootContext() throws Exception {
        // Create context metadata
        Map<String, String> metadata = new HashMap<>();
        metadata.put("projectName", "Financial Analysis");
        metadata.put("userRole", "Financial Analyst");
        metadata.put("dataSource", "Q1 2025 Financial Reports");
        
        // 1. Create a new root context
        RootContext context = contextManager.createRootContext("Financial Analysis Session", metadata);
        String contextId = context.getId();
        
        System.out.println("Created context: " + contextId);
        
        // 2. First interaction
        McpResponse response1 = client.sendPrompt(
            "Analyze the trends in Q1 financial data for our technology division",
            contextId
        );
        
        System.out.println("First response: " + response1.getGeneratedText());
        
        // 3. Update context with important information gained from response
        contextManager.addContextMetadata(contextId, 
            Map.of("identifiedTrend", "Increasing cloud infrastructure costs"));
        
        // Second interaction - using the same context
        McpResponse response2 = client.sendPrompt(
            "What's driving the increase in cloud infrastructure costs?",
            contextId
        );
        
        System.out.println("Second response: " + response2.getGeneratedText());
        
        // 4. Generate a summary of the analysis session
        McpResponse summaryResponse = client.sendPrompt(
            "Summarize our analysis of the technology division financials in 3-5 key points",
            contextId
        );
        
        // Store the summary in context metadata
        contextManager.addContextMetadata(contextId, 
            Map.of("analysisSummary", summaryResponse.getGeneratedText()));
            
        // Get updated context information
        RootContext updatedContext = contextManager.getRootContext(contextId);
        
        System.out.println("Context Information:");
        System.out.println("- Created: " + updatedContext.getCreatedAt());
        System.out.println("- Last Updated: " + updatedContext.getLastUpdatedAt());
        System.out.println("- Analysis Summary: " + 
            updatedContext.getMetadata().get("analysisSummary"));
            
        // 5. Archive context when done
        contextManager.archiveContext(contextId);
        System.out.println("Context archived");
    }
}
```

Στον παραπάνω κώδικα έχουμε:

1. Δημιουργήσει ένα root context για μια συνεδρία χρηματοοικονομικής ανάλυσης.
2. Στείλει πολλαπλά μηνύματα μέσα σε αυτό το context, επιτρέποντας στο μοντέλο να διατηρεί την κατάσταση.
3. Ενημερώσει το context με σχετικά μεταδεδομένα βάσει της συνομιλίας.
4. Δημιουργήσει μια περίληψη της συνεδρίας ανάλυσης και την αποθήκευσε στα μεταδεδομένα του context.
5. Αρχειοθετήσει το context όταν η συνομιλία ολοκληρώθηκε.

## Παράδειγμα: Διαχείριση Root Context

Η αποτελεσματική διαχείριση των root contexts είναι κρίσιμη για τη διατήρηση του ιστορικού συνομιλίας και της κατάστασης. Παρακάτω υπάρχει ένα παράδειγμα υλοποίησης διαχείρισης root context.

### Υλοποίηση σε JavaScript

```javascript
// JavaScript Example: Managing MCP Root Contexts
const { McpClient, RootContextManager } = require('@mcp/client');

class ContextSession {
  constructor(serverUrl, apiKey = null) {
    // Initialize the MCP client
    this.client = new McpClient({
      serverUrl,
      apiKey
    });
    
    // Initialize context manager
    this.contextManager = new RootContextManager(this.client);
  }
  
  /**
   * Create a new conversation context
   * @param {string} sessionName - Name of the conversation session
   * @param {Object} metadata - Additional metadata for the context
   * @returns {Promise<string>} - Context ID
   */
  async createConversationContext(sessionName, metadata = {}) {
    try {
      const contextResult = await this.contextManager.createRootContext({
        name: sessionName,
        metadata: {
          ...metadata,
          createdAt: new Date().toISOString(),
          status: 'active'
        }
      });
      
      console.log(`Created root context '${sessionName}' with ID: ${contextResult.id}`);
      return contextResult.id;
    } catch (error) {
      console.error('Error creating root context:', error);
      throw error;
    }
  }
  
  /**
   * Send a message in an existing context
   * @param {string} contextId - The root context ID
   * @param {string} message - The user's message
   * @param {Object} options - Additional options
   * @returns {Promise<Object>} - Response data
   */
  async sendMessage(contextId, message, options = {}) {
    try {
      // Send the message using the specified context
      const response = await this.client.sendPrompt(message, {
        rootContextId: contextId,
        temperature: options.temperature || 0.7,
        allowedTools: options.allowedTools || []
      });
      
      // Optionally store important insights from the conversation
      if (options.storeInsights) {
        await this.storeConversationInsights(contextId, message, response.generatedText);
      }
      
      return {
        message: response.generatedText,
        toolCalls: response.toolCalls || [],
        contextId
      };
    } catch (error) {
      console.error(`Error sending message in context ${contextId}:`, error);
      throw error;
    }
  }
  
  /**
   * Store important insights from a conversation
   * @param {string} contextId - The root context ID
   * @param {string} userMessage - User's message
   * @param {string} aiResponse - AI's response
   */
  async storeConversationInsights(contextId, userMessage, aiResponse) {
    try {
      // Extract potential insights (in a real app, this would be more sophisticated)
      const combinedText = userMessage + "\n" + aiResponse;
      
      // Simple heuristic to identify potential insights
      const insightWords = ["important", "key point", "remember", "significant", "crucial"];
      
      const potentialInsights = combinedText
        .split(".")
        .filter(sentence => 
          insightWords.some(word => sentence.toLowerCase().includes(word))
        )
        .map(sentence => sentence.trim())
        .filter(sentence => sentence.length > 10);
      
      // Store insights in context metadata
      if (potentialInsights.length > 0) {
        const insights = {};
        potentialInsights.forEach((insight, index) => {
          insights[`insight_${Date.now()}_${index}`] = insight;
        });
        
        await this.contextManager.updateContextMetadata(contextId, insights);
        console.log(`Stored ${potentialInsights.length} insights in context ${contextId}`);
      }
    } catch (error) {
      console.warn('Error storing conversation insights:', error);
      // Non-critical error, so just log warning
    }
  }
  
  /**
   * Get summary information about a context
   * @param {string} contextId - The root context ID
   * @returns {Promise<Object>} - Context information
   */
  async getContextInfo(contextId) {
    try {
      const contextInfo = await this.contextManager.getContextInfo(contextId);
      
      return {
        id: contextInfo.id,
        name: contextInfo.name,
        created: new Date(contextInfo.createdAt).toLocaleString(),
        lastUpdated: new Date(contextInfo.lastUpdatedAt).toLocaleString(),
        messageCount: contextInfo.messageCount,
        metadata: contextInfo.metadata,
        status: contextInfo.status
      };
    } catch (error) {
      console.error(`Error getting context info for ${contextId}:`, error);
      throw error;
    }
  }
  
  /**
   * Generate a summary of the conversation in a context
   * @param {string} contextId - The root context ID
   * @returns {Promise<string>} - Generated summary
   */
  async generateContextSummary(contextId) {
    try {
      // Ask the model to generate a summary of the conversation so far
      const response = await this.client.sendPrompt(
        "Please summarize our conversation so far in 3-4 sentences, highlighting the main points discussed.",
        { rootContextId: contextId, temperature: 0.3 }
      );
      
      // Store the summary in context metadata
      await this.contextManager.updateContextMetadata(contextId, {
        conversationSummary: response.generatedText,
        summarizedAt: new Date().toISOString()
      });
      
      return response.generatedText;
    } catch (error) {
      console.error(`Error generating context summary for ${contextId}:`, error);
      throw error;
    }
  }
  
  /**
   * Archive a context when it's no longer needed
   * @param {string} contextId - The root context ID
   * @returns {Promise<Object>} - Result of the archive operation
   */
  async archiveContext(contextId) {
    try {
      // Generate a final summary before archiving
      const summary = await this.generateContextSummary(contextId);
      
      // Archive the context
      await this.contextManager.archiveContext(contextId);
      
      return {
        status: "archived",
        contextId,
        summary
      };
    } catch (error) {
      console.error(`Error archiving context ${contextId}:`, error);
      throw error;
    }
  }
}

// Example usage
async function demonstrateContextSession() {
  const session = new ContextSession('https://mcp-server-example.com');
  
  try {
    // 1. Create a new context for a product support conversation
    const contextId = await session.createConversationContext(
      'Product Support - Database Performance',
      {
        customer: 'Globex Corporation',
        product: 'Enterprise Database',
        severity: 'Medium',
        supportAgent: 'AI Assistant'
      }
    );
    
    // 2. First message in the conversation
    const response1 = await session.sendMessage(
      contextId,
      "I'm experiencing slow query performance on our database cluster after the latest update.",
      { storeInsights: true }
    );
    console.log('Response 1:', response1.message);
    
    // Follow-up message in the same context
    const response2 = await session.sendMessage(
      contextId,
      "Yes, we've already checked the indexes and they seem to be properly configured.",
      { storeInsights: true }
    );
    console.log('Response 2:', response2.message);
    
    // 3. Get information about the context
    const contextInfo = await session.getContextInfo(contextId);
    console.log('Context Information:', contextInfo);
    
    // 4. Generate and display conversation summary
    const summary = await session.generateContextSummary(contextId);
    console.log('Conversation Summary:', summary);
    
    // 5. Archive the context when done
    const archiveResult = await session.archiveContext(contextId);
    console.log('Archive Result:', archiveResult);
    
    // 6. Handle any errors gracefully
  } catch (error) {
    console.error('Error in context session demonstration:', error);
  }
}

demonstrateContextSession();
```

Στον παραπάνω κώδικα έχουμε:

1. Δημιουργήσει ένα root context για μια συνομιλία υποστήριξης προϊόντος με τη συνάρτηση `createConversationContext`. Σε αυτή την περίπτωση, το context αφορά προβλήματα απόδοσης βάσης δεδομένων.

1. Στείλει πολλαπλά μηνύματα μέσα σε αυτό το context, επιτρέποντας στο μοντέλο να διατηρεί την κατάσταση με τη συνάρτηση `sendMessage`. Τα μηνύματα αφορούν αργή απόδοση ερωτημάτων και ρύθμιση ευρετηρίων.

1. Ενημερώσει το context με σχετικά μεταδεδομένα βάσει της συνομιλίας.

1. Δημιουργήσει μια περίληψη της συνομιλίας και την αποθήκευσε στα μεταδεδομένα του context με τη συνάρτηση `generateContextSummary`.

1. Αρχειοθετήσει το context όταν η συνομιλία ολοκληρώθηκε με τη συνάρτηση `archiveContext`.

1. Διαχειρίστηκε τα σφάλματα με ομαλό τρόπο για να εξασφαλίσει αξιοπιστία.

## Root Context για Βοήθεια Πολλαπλών Βημάτων

Σε αυτό το παράδειγμα, θα δημιουργήσουμε ένα root context για μια συνεδρία βοήθειας πολλαπλών βημάτων, δείχνοντας πώς να διατηρείται η κατάσταση σε πολλαπλές αλληλεπιδράσεις.

### Υλοποίηση σε Python

```python
# Python Example: Root Context for Multi-Turn Assistance
import asyncio
from datetime import datetime
from mcp_client import McpClient, RootContextManager

class AssistantSession:
    def __init__(self, server_url, api_key=None):
        self.client = McpClient(server_url=server_url, api_key=api_key)
        self.context_manager = RootContextManager(self.client)
    
    async def create_session(self, name, user_info=None):
        """Create a new root context for an assistant session"""
        metadata = {
            "session_type": "assistant",
            "created_at": datetime.now().isoformat(),
        }
        
        # Add user information if provided
        if user_info:
            metadata.update({f"user_{k}": v for k, v in user_info.items()})
            
        # Create the root context
        context = await self.context_manager.create_root_context(name, metadata)
        return context.id
    
    async def send_message(self, context_id, message, tools=None):
        """Send a message within a root context"""
        # Create options with context ID
        options = {
            "root_context_id": context_id
        }
        
        # Add tools if specified
        if tools:
            options["allowed_tools"] = tools
        
        # Send the prompt within the context
        response = await self.client.send_prompt(message, options)
        
        # Update context metadata with conversation progress
        await self.context_manager.update_context_metadata(
            context_id,
            {
                f"message_{datetime.now().timestamp()}": message[:50] + "...",
                "last_interaction": datetime.now().isoformat()
            }
        )
        
        return response
    
    async def get_conversation_history(self, context_id):
        """Retrieve conversation history from a context"""
        context_info = await self.context_manager.get_context_info(context_id)
        messages = await self.client.get_context_messages(context_id)
        
        return {
            "context_info": context_info,
            "messages": messages
        }
    
    async def end_session(self, context_id):
        """End an assistant session by archiving the context"""
        # Generate a summary prompt first
        summary_response = await self.client.send_prompt(
            "Please summarize our conversation and any key points or decisions made.",
            {"root_context_id": context_id}
        )
        
        # Store summary in metadata
        await self.context_manager.update_context_metadata(
            context_id,
            {
                "summary": summary_response.generated_text,
                "ended_at": datetime.now().isoformat(),
                "status": "completed"
            }
        )
        
        # Archive the context
        await self.context_manager.archive_context(context_id)
        
        return {
            "status": "completed",
            "summary": summary_response.generated_text
        }

# Example usage
async def demo_assistant_session():
    assistant = AssistantSession("https://mcp-server-example.com")
    
    # 1. Create session
    context_id = await assistant.create_session(
        "Technical Support Session",
        {"name": "Alex", "technical_level": "advanced", "product": "Cloud Services"}
    )
    print(f"Created session with context ID: {context_id}")
    
    # 2. First interaction
    response1 = await assistant.send_message(
        context_id, 
        "I'm having trouble with the auto-scaling feature in your cloud platform.",
        ["documentation_search", "diagnostic_tool"]
    )
    print(f"Response 1: {response1.generated_text}")
    
    # Second interaction in the same context
    response2 = await assistant.send_message(
        context_id,
        "Yes, I've already checked the configuration settings you mentioned, but it's still not working."
    )
    print(f"Response 2: {response2.generated_text}")
    
    # 3. Get history
    history = await assistant.get_conversation_history(context_id)
    print(f"Session has {len(history['messages'])} messages")
    
    # 4. End session
    end_result = await assistant.end_session(context_id)
    print(f"Session ended with summary: {end_result['summary']}")

if __name__ == "__main__":
    asyncio.run(demo_assistant_session())
```

Στον παραπάνω κώδικα έχουμε:

1. Δημιουργήσει ένα root context για μια συνεδρία τεχνικής υποστήριξης με τη συνάρτηση `create_session`. Το context περιλαμβάνει πληροφορίες χρήστη όπως όνομα και τεχνικό επίπεδο.

1. Στείλει πολλαπλά μηνύματα μέσα σε αυτό το context, επιτρέποντας στο μοντέλο να διατηρεί την κατάσταση με τη συνάρτηση `send_message`. Τα μηνύματα αφορούν προβλήματα με τη λειτουργία αυτόματης κλιμάκωσης.

1. Ανακτήσει το ιστορικό συνομιλίας χρησιμοποιώντας τη συνάρτηση `get_conversation_history`, που παρέχει πληροφορίες context και μηνύματα.

1. Τερμάτισε τη συνεδρία αρχειοθετώντας το context και δημιουργώντας μια περίληψη με τη συνάρτηση `end_session`. Η περίληψη καταγράφει τα βασικά σημεία της συνομιλίας.

## Βέλτιστες Πρακτικές για Root Context

Ακολουθούν μερικές βέλτιστες πρακτικές για την αποτελεσματική διαχείριση των root contexts:

- **Δημιουργήστε Εστιασμένα Contexts**: Δημιουργήστε ξεχωριστά root contexts για διαφορετικούς σκοπούς ή τομείς συνομιλίας για να διατηρείτε την σαφήνεια.

- **Ορίστε Πολιτικές Λήξης**: Εφαρμόστε πολιτικές για αρχειοθέτηση ή διαγραφή παλαιών contexts για τη διαχείριση αποθηκευτικού χώρου και τη συμμόρφωση με πολιτικές διατήρησης δεδομένων.

- **Αποθηκεύστε Σχετικά Μεταδεδομένα**: Χρησιμοποιήστε τα μεταδεδομένα του context για να αποθηκεύετε σημαντικές πληροφορίες της συνομιλίας που μπορεί να είναι χρήσιμες αργότερα.

- **Χρησιμοποιήστε Συνεπή Αναγνωριστικά Context**: Μόλις δημιουργηθεί ένα context, χρησιμοποιήστε το αναγνωριστικό του με συνέπεια για όλα τα σχετικά αιτήματα για να διατηρείτε τη συνέχεια.

- **Δημιουργήστε Περιλήψεις**: Όταν ένα context μεγαλώνει πολύ, σκεφτείτε να δημιουργήσετε περιλήψεις για να καταγράψετε τις βασικές πληροφορίες ενώ διαχειρίζεστε το μέγεθος του context.

- **Εφαρμόστε Έλεγχο Πρόσβασης**: Για συστήματα με πολλούς χρήστες, εφαρμόστε κατάλληλους ελέγχους πρόσβασης για να διασφαλίσετε την ιδιωτικότητα και την ασφάλεια των contexts συνομιλίας.

- **Διαχειριστείτε Περιορισμούς Context**: Να είστε ενήμεροι για τους περιορισμούς μεγέθους του context και εφαρμόστε στρατηγικές για τη διαχείριση πολύ μεγάλων συνομιλιών.

- **Αρχειοθετήστε Όταν Ολοκληρωθεί**: Αρχειοθετήστε τα contexts όταν οι συνομιλίες ολοκληρωθούν για να ελευθερώσετε πόρους διατηρώντας παράλληλα το ιστορικό συνομιλίας.

## Τι ακολουθεί

- [5.5 Routing](../mcp-routing/README.md)

**Αποποίηση ευθυνών**:  
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία αυτόματης μετάφρασης AI [Co-op Translator](https://github.com/Azure/co-op-translator). Παρόλο που επιδιώκουμε την ακρίβεια, παρακαλούμε να γνωρίζετε ότι οι αυτόματες μεταφράσεις ενδέχεται να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη γλώσσα του θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για τυχόν παρεξηγήσεις ή λανθασμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.