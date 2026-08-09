# RAG (Retrieval Augmented Generation) – Complete Pipeline

**RAG (Retrieval Augmented Generation)** ek technique hai jisme LLM ko answer generate karne se pehle external/private knowledge base se relevant information provide ki jaati hai.

RAG ko mainly **2 pipelines** mein divide kiya jaata hai:

1. **Data Ingestion Pipeline**
2. **Query Retrieval & Generation Pipeline**

---

# 1. Data Ingestion Pipeline

Data Ingestion Pipeline ka main purpose hai:

> **Raw data ko process karke aise format mein convert karna jise Vector Database mein store kiya ja sake aur future mein efficiently retrieve kiya ja sake.**

Is pipeline mein actual user query nahi hoti. Yeh mostly **pre-processing / preparation phase** hai.

## Overall Flow

```text
Raw Data
   ↓
Data Parsing
   ↓
Document Structure + Metadata
   ↓
Chunking
   ↓
Embedding
   ↓
Vector Database
```

## Step 1: Data Ingestion

Sabse pehle system mein different sources se data aata hai.

```text
PDF
HTML
Excel
Word Documents
Database
Text Files
Web Pages
Company Documents
```

Example:

```text
Employee Leave Policy.pdf

        ↓ Data Ingestion

"An employee is entitled to 12 casual leaves
per year..."
```

Yeh raw document hamare RAG system mein input ke roop mein aayega.

---

## Step 2: Data Parsing

Raw document directly embedding ke liye suitable nahi hota.

Isliye pehle usko **parse** kiya jaata hai.

### Data Parsing ka meaning

> Different file formats se useful text aur information extract karna.

```text
PDF   → Text
HTML  → Text
Excel → Rows / Columns
Word  → Text
DB    → Records
```

Example:

```text
Employee Leave Policy.pdf

        ↓ Data Parsing

"An employee is entitled to 12 casual leaves..."
```

Parsing ke time sirf text hi nahi, balki document ki useful information bhi preserve ki ja sakti hai.

### Metadata

Document ke saath metadata bhi store kiya ja sakta hai:

```text
document_name
page_number
department
created_date
category
author
source
```

Example:

```text
Text:
"An employee is entitled to 12 casual leaves..."

Metadata:
{
   document: "Employee Leave Policy.pdf",
   page: 5,
   category: "HR",
   department: "Human Resource"
}
```

Yeh metadata baad mein retrieval ko improve karne mein useful hota hai.

---

# Step 3: Chunking

Ab maan lo hamare paas ek **100-page PDF** hai.

Hum poori PDF ko ek hi vector mein convert nahi karna chahenge.

Isliye document ko chhote-chhote pieces mein divide kiya jaata hai.

In pieces ko **Chunks** kehte hain.

```text
Large Document
       ↓
 ┌─────────────┐
 │   Chunk 1   │
 ├─────────────┤
 │   Chunk 2   │
 ├─────────────┤
 │   Chunk 3   │
 ├─────────────┤
 │   Chunk 4   │
 └─────────────┘
```

Example:

```text
100 Page PDF
      ↓
Chunk 1 → Page 1-3
Chunk 2 → Page 3-5
Chunk 3 → Page 5-7
Chunk 4 → Page 7-9
...
```

Chunking fixed pages ke basis par hi ho zaroori nahi hai. Chunking **characters, tokens, paragraphs, sentences ya semantic meaning** ke basis par bhi ho sakti hai.

### Chunking kyun zaroori hai?

- LLM ki context limit hoti hai.
- Embedding model ko manageable text dena hota hai.
- Retrieval ke time relevant information ka small portion chahiye.
- Chhote chunks se relevant information accurately retrieve ho sakti hai.

---

# Step 4: Embedding

Ab hamare paas chunks hain.

Example:

```text
Chunk 1:
"Employees are entitled to 12 casual leaves..."

Chunk 2:
"Employees can apply for leave through HR portal..."

Chunk 3:
"Medical leave requires a doctor's certificate..."
```

Computer directly in sentences ka **meaning mathematically understand/search** nahi kar sakta.

Isliye hum **Embedding Model** use karte hain.

Embedding ka kaam:

> **Text ko numerical vector mein convert karna.**

Example:

```text
Chunk 1
   ↓
Embedding Model
   ↓
[0.21, -0.45, 0.78, 0.12, ...]
```

Similarly:

```text
Chunk 2
   ↓
Embedding Model
   ↓
[0.11, -0.32, 0.81, 0.17, ...]
```

Ye numbers collectively **Vector / Embedding** kehlate hain.

### Semantic Similarity

Similar meaning wale texts ke vectors vector space mein relatively close hote hain.

Example:

```text
"How many casual leaves are available?"
```

aur

```text
"Employees are entitled to 12 casual leaves."
```

Words exactly same nahi hain, lekin meaning similar hai.

Embedding model in dono ko semantically close vectors mein represent kar sakta hai.

---

# Step 5: Vector Database

Ab embeddings ko store karne ke liye **Vector Database** use hota hai.

Examples:

```text
ChromaDB
FAISS
Pinecone
Weaviate
Milvus
```

Vector DB mein generally hum store karte hain:

```text
Vector
+
Original Text / Chunk
+
Metadata
```

Example:

```text
┌───────────────────────────────────────┐
│             Vector DB                 │
├───────────────────────────────────────┤
│ Vector       │ Text       │ Metadata  │
├───────────────────────────────────────┤
│ [0.21,...]   │ Chunk 1    │ Page 5    │
│ [0.11,...]   │ Chunk 2    │ Page 6    │
│ [0.81,...]   │ Chunk 3    │ Page 7    │
└───────────────────────────────────────┘
```

Ab hamara **Data Ingestion Pipeline complete** ho gaya.

---

# Data Ingestion ka Complete Flow

Paper par isko simple tarike se aise bana sakte ho:

```text
       DATA INGESTION PIPELINE
                 │
                 ▼
        ┌─────────────────┐
        │    Raw Data     │
        │ PDF / HTML /    │
        │ Excel / DB      │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Data Parsing   │
        │ Extract Text +  │
        │ Metadata        │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    Chunking     │
        │ Chunk 1         │
        │ Chunk 2         │
        │ Chunk 3         │
        │ Chunk 4         │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    Embedding    │
        │   Text → Vector │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   Vector DB     │
        │ Store Vectors + │
        │ Text + Metadata │
        └─────────────────┘
```

---

# 2. Query Retrieval & Generation Pipeline

Ab Data Ingestion complete ho chuka hai.

Vector Database ke andar hamara knowledge stored hai.

Ab **user query karta hai**.

Example:

```text
User:
"How many casual leaves can an employee take?"
```

Ab doosri pipeline start hoti hai.

---

## Step 1: User Query

```text
User Query
    ↓
"How many casual leaves
 can an employee take?"
```

---

## Step 2: Query Embedding

User ki query ko bhi **same/suitable embedding model** se vector mein convert kiya jaata hai.

```text
User Query
     ↓
Embedding Model
     ↓
[0.19, -0.42, 0.76, ...]
```

Ab query bhi vector ban gayi.

---

# Step 3: Similarity Search / Retrieval

Ab query vector ko Vector Database mein search kiya jaata hai.

Vector DB dekhta hai:

> Kaunse stored vectors user ki query ke meaning ke sabse close hain?

Is process ko **Similarity Search** kehte hain.

Common similarity measures:

```text
Cosine Similarity
Euclidean Distance
Dot Product
```

Example:

```text
Query Vector
     │
     ▼
┌────────────────────┐
│    Vector DB       │
│                    │
│ Chunk 1 → 95%      │ ← Relevant
│ Chunk 2 → 82%      │
│ Chunk 3 → 40%      │
│ Chunk 4 → 91%      │ ← Relevant
└────────────────────┘
```

Top relevant chunks retrieve kiye jaate hain.

---

# Step 4: Context

Retrieved chunks ko **Context** kaha jaata hai.

Example:

```text
Query:
"How many casual leaves can an employee take?"

Retrieved Context:

Chunk 1:
"Employees are entitled to 12 casual
leaves per year."
```

Ab LLM ko relevant information mil gayi.

---

# Step 5: Augmentation

Yahan RAG ka main concept aata hai.

Hum combine karte hain:

```text
User Query
     +
Retrieved Context
     +
System Prompt / Instructions
```

Example:

```text
Context:
Employees are entitled to 12 casual
leaves per year.

Query:
How many casual leaves can an employee take?

Instruction:
Answer only using the provided context.
```

Ye complete input LLM ko diya jaata hai.

---

# Step 6: Generation

Finally:

```text
Context + Query + Prompt
             ↓
            LLM
             ↓
          Answer
```

LLM answer generate karta hai:

> "An employee is entitled to 12 casual leaves per year."

---

# Complete RAG Pipeline – Paper Diagram

Tumhare original diagram ko paper par **left-to-right** layout mein is tarah bana sakte ho:

```text
                 RAG PIPELINE
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
 DATA INGESTION PIPELINE   QUERY RETRIEVAL PIPELINE
          │                       │
          ▼                       ▼
     Raw Documents           User Query
     PDF / HTML /             │
     Excel / DB              ▼
          │                Embedding
          ▼                   │
     Data Parsing             ▼
          │              Query Vector
          ▼                   │
       Chunking               ▼
          │              Similarity Search
          ▼                   │
      Embedding               ▼
          │              Relevant Chunks
          ▼                   │
     Vector Database          ▼
          │                 Context
          │                   │
          │                   ▼
          │             Query + Context
          │                   │
          │                   ▼
          │                  LLM
          │                   │
          │                   ▼
          │                 Answer
          │
          └────────────► Vector DB
```

---

# Recommended Technically Correct Diagram

Tumhari original image mein **Embedding → Vector DB → Similarity Search** dikhaya gaya hai.

Technically, **Similarity Search query/retrieval phase ka part hai**, Data Ingestion phase ka nahi.

Isliye paper par best architecture:

```text
                 DATA INGESTION
                      │
                      ▼
                   Chunking
                      │
                      ▼
                   Embedding
                      │
                      ▼
                ┌───────────┐
                │ VECTOR DB │
                └─────┬─────┘
                      ▲
                      │
                Similarity Search
                      │
                  Query Vector
                      ▲
                      │
                     Query
```

Aur complete retrieval flow:

```text
User Query
    │
    ▼
Query Embedding
    │
    ▼
Query Vector
    │
    ▼
┌────────────────┐
│   Vector DB    │
│                │
│ Similarity     │
│ Search         │
└───────┬────────┘
        │
        ▼
Relevant Chunks
        │
        ▼
     Context
        │
        ├──────────────┐
        │              │
        ▼              ▼
      Query         Prompt
        │              │
        └──────┬───────┘
               ▼
              LLM
               │
               ▼
             Answer
```

---

# RAG Kyun Zaroori Hai?

## 1. Hallucination Reduce Karna

Sirf LLM ka use karne par model kabhi-kabhi incorrect information generate kar sakta hai.

RAG relevant external context provide karta hai, jisse answer available knowledge par grounded hota hai.

## 2. Private Data

Companies apna internal data use kar sakti hain:

```text
HR Policies
Finance Documents
Internal Documentation
Product Information
Customer Data
```

Bina model ko baar-baar retrain kiye.

## 3. Latest / Changing Information

Agar knowledge base update hota rehta hai, toh updated documents ko Vector DB mein ingest kiya ja sakta hai.

Har baar LLM ko retrain karna zaroori nahi hota.

## 4. Cost Effective

Fine-tuning ya complete model retraining ki comparison mein RAG kai use cases mein simpler aur cost-effective approach hoti hai.

---

# One-Line Summary

```text
Data → Parse → Chunk → Embed → Store in Vector DB
                                      ↓
User Query → Embed → Similarity Search → Context
                                      ↓
                            Query + Context → LLM
                                      ↓
                                    Answer
```

> **Simple words mein: RAG pehle apne data ko samajhkar Vector Database mein store karta hai, phir user ke question ke according relevant information retrieve karke LLM ko deta hai, aur LLM us context ke basis par answer generate karta hai.**
