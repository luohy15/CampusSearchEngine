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
	private float avgTitleLen = 1.0f; // omg why initially 1?
	private float avgBodyLen = 1.0f; // follow stupid hack

	private static float TITLE_BOOST = 500.0f;
	private static float BODY_BOOST = 1.0f;
	private static float PR_QUANTUM = 1e-8f;
	private static String TXT_PATH = "/home/fuck/hw3/ImageSearch/DataParser/build";

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
			System.out.println("INFO saving avgTitleLen: " + avgTitleLen);
			pw.println(avgTitleLen);
			System.out.println("INFO saving avgBodyLen: " + avgBodyLen);
			pw.println(avgBodyLen);
			pw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private float pr2docBoost(float pr) {
		// some nonlinearity here
		return (float) (Math.log(pr / PR_QUANTUM) + 1.0f);
	}

	private Document buildDocument(NamedNodeMap attrs) throws FileNotFoundException {
		Document document = new Document();
		// title field
		String titleString = attrs.getNamedItem("title").getNodeValue();
		Field titleField = new Field("title", titleString, Field.Store.YES,
				Field.Index.ANALYZED);
		titleField.setBoost(TITLE_BOOST);
		document.add(titleField);
		// body field
		String txtFilePath = TXT_PATH + "/" + attrs.getNamedItem("id").getNodeValue() + ".txt"; 
		String bodyString = readContent(txtFilePath);
		Field bodyField = new Field("body", bodyString, Field.Store.YES,
				Field.Index.ANALYZED);
		bodyField.setBoost(BODY_BOOST);
		document.add(bodyField);
		// title field
		String urlString = attrs.getNamedItem("url").getNodeValue();
		Field urlField = new Field("url", urlString, Field.Store.YES,
				Field.Index.NO);
		document.add(urlField);
		// page rank boost
		float pr = Float.parseFloat(attrs.getNamedItem("pr").getNodeValue());
		document.setBoost(pr2docBoost(pr));
		return document;
	}
	
	private String readContent(String txtFilePath) throws FileNotFoundException {
		// extract line[4] (starting from 0)
		Scanner scanner = new Scanner(new File(txtFilePath));
		for (int i = 0; i < 4; i++)
			scanner.nextLine(); // skip line 0..3
		assert(scanner.hasNextLine());
		String retval = scanner.nextLine();
		scanner.close();
		return retval;
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
				Document document = buildDocument(attrs);
				indexWriter.addDocument(document);
				System.out.println("title=" + document.get("title") + " prboost=" +
						document.getBoost());
				// other stupid stuff
				avgTitleLen += document.get("title").length();  // stupid hack 
				avgBodyLen += document.get("body").length();
			}
			avgTitleLen /= indexWriter.numDocs();
			avgBodyLen /= indexWriter.numDocs();
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
