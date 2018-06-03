import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.wltea.analyzer.lucene.IKAnalyzer;

public class HighLighter {
	public class Pair<T1, T2> {
		public T1 v1;
		public T2 v2;
		public Pair(T1 a, T2 b) {
			v1 = a;
			v2 = b;
		}
	}

	ArrayList<String> terms = new ArrayList<String>();

	public HighLighter(String queryString) throws IOException {
		tokenizeQueryString(queryString);
	}

	private void tokenizeQueryString(String queryString) throws IOException {
		Analyzer analyzer = new IKAnalyzer();
		StringReader reader = new StringReader(queryString);
		TokenStream ts = analyzer.tokenStream("", reader);
		CharTermAttribute term = ts.getAttribute(CharTermAttribute.class);
		while (ts.incrementToken()) {
			String queryTerm = term.toString();
			System.out.println(queryTerm);
			terms.add(queryTerm);
		}
		analyzer.close();
		reader.close();
	}

	private static final int N_CONTEXT = 5;
	private static final int N_NONFULL_TRIM = 100;
	private static final String HL_SEP = "...";
	
	public String highlight(String text, boolean full) {
		if (full) {
			for (String t : terms) {
				text = text.replace(t, "<span style=\"color:red;\">" + t + "</span>");
			}
			return text;
		} else {
			// holy shxt after writing so much C, I forgot how to write OO code
			// 	so below is written actually in C

			// find individual display interval
			ArrayList<Pair<Integer, Integer>> raw_intvls = new ArrayList<Pair<Integer, Integer>>();
			for (String t : terms) {
				int idx = 0;
				while (true) {
					idx = text.indexOf(t, idx);
					if (idx == -1)
						break;
					raw_intvls.add(new Pair<Integer, Integer>(
							Math.max(0, idx - N_CONTEXT),
							Math.min(text.length(), idx + t.length() + N_CONTEXT)));
					idx += t.length();
				}
			}

			// merge
			ArrayList<Pair<Integer, Integer>> intvls = new ArrayList<Pair<Integer, Integer>>();
			for (int i = 0; i < raw_intvls.size(); i++) {
				Pair<Integer, Integer> p = raw_intvls.get(i);
				int bi = p.v1;
				int ei = p.v2;
				int flag = 0;
				for (int j = 0; j < intvls.size(); j++) {
					Pair<Integer, Integer> p2 = intvls.get(j);
					int mbj = p2.v1;
					int mej = p2.v2;
					if (ei >= mbj && ei < mej && bi < mbj) {
						intvls.set(j, new Pair<Integer, Integer>(bi, mej));
						flag = 2;
						break;
					}
					if (bi >= mbj && bi < mej && ei > mej) {
						intvls.set(j, new Pair<Integer, Integer>(mbj, ei));
						flag = 2;
						break;
					}
					if (bi >= mbj && ei <= mej) {
						flag = 1;
						break;
					}
				}
				switch (flag) {
				case 0: // no overlap, not contained in any other
					intvls.add(new Pair<Integer, Integer>(bi, ei));
					break;
				case 1: // totally contained
					break;
				case 2: // overlap but not contained
					break;
				default: // wtf?
					assert (false);
				}
			}
			// TODO: sort
			// construct output
			StringBuilder sb = new StringBuilder();
			String rv = null;
			sb.append(HL_SEP);
			for (int i = 0; i < intvls.size(); i++) {
				Pair<Integer, Integer> p2 = intvls.get(i);
				int mbj = p2.v1;
				int mej = p2.v2;
				sb = sb.append(text.substring(mbj, mej));
				sb = sb.append(HL_SEP);
				if (sb.length() >= N_NONFULL_TRIM) {
					rv = sb.substring(0, N_NONFULL_TRIM);
					break;
				}
			}
			if (rv == null)
				rv = sb.toString();
			return highlight(rv, true);
		}
	}
}
