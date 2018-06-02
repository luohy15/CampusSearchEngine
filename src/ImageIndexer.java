import java.io.*;
import java.util.*;

import org.w3c.dom.*;
import org.wltea.analyzer.lucene.IKAnalyzer;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import javax.xml.parsers.*;

public class ImageIndexer {
	private Analyzer analyzer;
	private IndexWriter indexWriter;
	private float averageLength = 1.0f;

	public ImageIndexer(String indexDir) {
		analyzer = new IKAnalyzer();
		try {
			IndexWriterConfig iwc = new IndexWriterConfig(Version.LUCENE_35, analyzer);
			Directory dir = FSDirectory.open(new File(indexDir));
			indexWriter = new IndexWriter(dir, iwc);
			indexWriter.setSimilarity(new SimpleSimilarity());
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void saveGlobals(String filename) {
		try {
			PrintWriter pw = new PrintWriter(new File(filename));
			pw.println(averageLength);
			pw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void indexSpecialFile(String filename) {
		try {
			// extract all <pic ...> ... </pic>
			DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
			DocumentBuilder db = dbf.newDocumentBuilder();
			org.w3c.dom.Document doc = db.parse(new File(filename));
			NodeList nodeList = doc.getElementsByTagName("pic");
			// for each <pic/>, build a Document for it
			for (int i = 0; i < nodeList.getLength(); i++) {
				// extract information
				Node node = nodeList.item(i);
				NamedNodeMap attrs = node.getAttributes();
				String absString = attrs.getNamedItem("bigClass").getNodeValue() + " "
						+ attrs.getNamedItem("smallClass").getNodeValue() + " "
						+ attrs.getNamedItem("query").getNodeValue();
				// build document
				Document document = new Document();
				Field abstractField = new Field("abstract", absString, Field.Store.YES, Field.Index.ANALYZED);
				document.add(abstractField);
				indexWriter.addDocument(document);
				// other stupid stuff
				averageLength += absString.length();				
				if (i % 10000 == 0) {
					System.out.println("process " + i);
				}
				// TODO: add other fields such as html title or html content

			}
			averageLength /= indexWriter.numDocs();
			System.out.println("average length = " + averageLength);
			System.out.println("total " + indexWriter.numDocs() + " documents");
			indexWriter.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		ImageIndexer indexer = new ImageIndexer("forIndex/index");
		indexer.indexSpecialFile("input/sogou-utf8.xml");
		indexer.saveGlobals("forIndex/global.txt");
	}
}
