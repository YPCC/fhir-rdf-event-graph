const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType, 
        ShadingType, PageNumber, LevelFormat } = require('docx');
const fs = require('fs');

// Define borders for tables
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

const doc = new Document({
  styles: {
    default: { 
      document: { 
        run: { font: "Arial", size: 22 } // 11pt default
      } 
    },
    paragraphStyles: [
      { 
        id: "Heading1", 
        name: "Heading 1", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1F4E79" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } 
      },
      { 
        id: "Heading2", 
        name: "Heading 2", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } 
      },
      { 
        id: "Heading3", 
        name: "Heading 3", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "5B9BD5" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } 
      }
    ]
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 }, // US Letter
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            alignment: AlignmentType.RIGHT,
            children: [
              new TextRun({ text: "FHIR-RDF Patient Event Graph POC", italics: true, size: 18, color: "666666" })
            ]
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Page ", size: 18 }),
              new TextRun({ children: [PageNumber.CURRENT], size: 18 }),
              new TextRun({ text: " of ", size: 18 }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18 })
            ]
          })
        ]
      })
    },
    children: [
      // Title
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [
          new TextRun({ text: "FHIR-RDF Patient Event Graph", bold: true, size: 48, color: "1F4E79" })
        ]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [
          new TextRun({ text: "Project Documentation", bold: true, size: 32, color: "2E75B6" })
        ]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [
          new TextRun({ text: "POC for Colorectal Cancer Patient Timeline Visualization", size: 22, italics: true, color: "666666" })
        ]
      }),

      // Problem Statement
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("1. Problem Statement")] }),
      
      new Paragraph({
        spacing: { after: 200 },
        children: [
          new TextRun("In oncology and chronic disease management, patient data is fragmented across multiple systems (EHRs, labs, imaging, pharmacy). Clinicians and researchers struggle to visualize the complete patient journey in a meaningful, chronological, and interconnected way.")
        ]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [
          new TextRun({ text: "Key Challenges:", bold: true })
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Raw FHIR data is difficult to explore interactively at scale")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("No standardized way to represent temporal event graphs for cancer patients")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Blank nodes and complex nested structures in FHIR RDF make visualization challenging")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Lack of integrated tools combining GraphDB exploration with Python-based timeline animations")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 300 },
        children: [new TextRun("Limited support for oncology-specific standards like mCODE in open-source tooling")]
      }),

      // Approach
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("2. Approach")] }),
      
      new Paragraph({
        spacing: { after: 200 },
        children: [
          new TextRun("We built an end-to-end pipeline that transforms FHIR patient data into a rich, queryable, and visualizable RDF knowledge graph with a strong focus on colorectal cancer journeys.")
        ]
      }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.1 Core Pipeline")] }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Data Ingestion: ", bold: true }), new TextRun("Fetch realistic colorectal patient bundles from public HAPI FHIR servers or Synthea synthetic data")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "FHIR → RDF Conversion: ", bold: true }), new TextRun("Use official HL7 FHIR RDF specification with proper handling of blank nodes (preserve or skolemize)")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Graph Enrichment: ", bold: true }), new TextRun("Add temporal sequencing (hasNextEvent) and optional mCODE oncology alignment")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "Visualization Layer: ", bold: true }), new TextRun("Interactive Plotly timelines + high-quality animated GIF patient journeys")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 200 },
        children: [new TextRun({ text: "Storage & Exploration: ", bold: true }), new TextRun("Native support for GraphDB (Free) with Visual Graph explorer and SPARQL")]
      }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.2 Key Innovations")] }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Blank node management strategy (preserve vs skolemize)")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Lightweight timeline ontology with hasNextEvent relationships")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("mCODE alignment for oncology interoperability")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 300 },
        children: [new TextRun("One-command Docker Compose stack (GraphDB + Streamlit web app)")]
      }),

      // Tech Stack
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("3. Technology Stack")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.1 Core Technologies")] }),
      new Table({
        width: { size: 10080, type: WidthType.DXA },
        columnWidths: [3600, 6480],
        rows: [
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 3600, type: WidthType.DXA }, shading: { fill: "1F4E79", type: ShadingType.CLEAR },
                children: [new Paragraph({ children: [new TextRun({ text: "Component", bold: true, color: "FFFFFF" })] })] }),
              new TableCell({ borders, width: { size: 6480, type: WidthType.DXA }, shading: { fill: "1F4E79", type: ShadingType.CLEAR },
                children: [new Paragraph({ children: [new TextRun({ text: "Technology", bold: true, color: "FFFFFF" })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 3600, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("FHIR Data")] })] }),
              new TableCell({ borders, width: { size: 6480, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("HL7 FHIR R4, HAPI FHIR Server, Synthea")] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 3600, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("RDF Layer")] })] }),
              new TableCell({ borders, width: { size: 6480, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("rdflib, fhirtordf, Turtle serialization")] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 3600, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Graph Database")] })] }),
              new TableCell({ borders, width: { size: 6480, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("GraphDB Free (Ontotext)")] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 3600, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Visualization")] })] }),
              new TableCell({ borders, width: { size: 6480, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Plotly, Matplotlib, NetworkX, Gephi")] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 3600, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Web Interface")] })] }),
              new TableCell({ borders, width: { size: 6480, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Streamlit")] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders, width: { size: 3600, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Validation & Ontology")] })] }),
              new TableCell({ borders, width: { size: 6480, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("PySHACL, OWL, mCODE IG")] })] })
            ]
          })
        ]
      }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 300 }, children: [new TextRun("3.2 Supporting Tools")] }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Docker & Docker Compose (one-command deployment)")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Jupyter Notebook (full interactive version)")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Python 3.11+ with pandas, requests, imageio")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 400 },
        children: [new TextRun("GitHub-ready project structure with MIT license")]
      }),

      // Conclusion
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("4. Project Value")] }),
      new Paragraph({
        spacing: { after: 200 },
        children: [
          new TextRun("This POC delivers a production-ready foundation for healthcare organizations and researchers who need to transform FHIR data into actionable, visual, and standards-compliant patient event graphs — with particular strength in oncology use cases.")
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/home/workdir/artifacts/fhir-rdf-event-graph/FHIR_RDF_Patient_Event_Graph_POC_Documentation.docx", buffer);
  console.log("Word document created successfully!");
});