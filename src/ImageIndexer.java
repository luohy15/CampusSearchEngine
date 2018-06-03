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

	private static float TITLE_BOOST = 10.0f;
	private static float BODY_BOOST = 1.0f;
	private static float PR_QUANTUM = 1e-8f;

	@SuppressWarnings("deprecation")
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

	private float pr2docBoost(float pr) {
		// some nonlinearity here
		return (float) (Math.log(pr / PR_QUANTUM) + 1.0f);
	}

	public void indexSpecialFile(String filename) {
		try {
			// extract all <pic ...> ... </pic>
			DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
			DocumentBuilder db = dbf.newDocumentBuilder();
			org.w3c.dom.Document doc = db.parse(new File(filename));
			NodeList nodeList = doc.getElementsByTagName("pic");
			System.out.println("INFO: found " + nodeList.getLength() + " entries");
			// for each <pic/>, build a Document for it
			for (int i = 0; i < nodeList.getLength(); i++) {
				// extract information
				NamedNodeMap attrs = nodeList.item(i).getAttributes();
				// build document
				Document document = new Document();
				String titleString = attrs.getNamedItem("title").getNodeValue();
				Field titleField = new Field("title", titleString, Field.Store.YES,
						Field.Index.ANALYZED);
				titleField.setBoost(TITLE_BOOST);
				document.add(titleField);
				float pr = Float.parseFloat(attrs.getNamedItem("pr").getNodeValue());
				document.setBoost(pr2docBoost(pr));
				System.out.println("title=" + titleString + " prboost=" +
						pr2docBoost(pr));
				indexWriter.addDocument(document);
				// other stupid stuff
				averageLength += titleString.length(); // TODO
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
		indexer.indexSpecialFile("input/html.xml");
		indexer.saveGlobals("forIndex/global.txt");
	}
}
