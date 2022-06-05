/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.lucene.htmlindexer;


import java.nio.charset.StandardCharsets;
import java.nio.file.FileSystems;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;

import com.opencsv.CSVWriter;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.LongPoint;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
//import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.RAMDirectory;


import java.io.*;  
import java.util.Scanner;


/** Index all text files under a directory.
 * <p>
 * This is a command-line application demonstrating simple Lucene indexing.
 * Run it with no command-line arguments for usage information.
 */


public class Searcher {

public static void main(String[] args) throws IOException,ParseException
{   
	boolean tester = true;
	String dataPath = "queryCache";
	File folder = new File(dataPath);
	File[] listOfFiles = folder.listFiles();
	int QueryMonitor = listOfFiles.length;
	System.out.println("qqqaaaaamonitor " + listOfFiles.length);
	while(tester) {
		listOfFiles = folder.listFiles();
		
		if(QueryMonitor == listOfFiles.length) {
			System.out.println("no query " + listOfFiles.length);
			try
			{
			    Thread.sleep(1000);
			}
			catch(InterruptedException ex)
			{
			    Thread.currentThread().interrupt();
			}
			continue;
		}
		
		QueryMonitor =listOfFiles.length;
		String querystr = "";
		String fileName = "";
		for ( int i =0;i< listOfFiles.length;i++) {
			fileName = dataPath+ "\\"+listOfFiles[i].getName();
			
			BufferedReader bri = new BufferedReader(new FileReader(fileName));     
			if (bri.readLine() == null) {
			    System.out.println("No errors, and file empty");
			    System.out.println("my queryaaaa: "+listOfFiles[i].getName());
			    querystr = listOfFiles[i].getName().substring(0, listOfFiles[i].getName().length() - 4);
			    System.out.println("my query: "+querystr);
			    break;
			}
			
		}
		System.out.println("updates");
		String perCSVFile = "fileRowIndexer.csv";
		BufferedReader br = new BufferedReader(new FileReader(perCSVFile));
		String line = "";
		ArrayList<StringIntegerPair> fileRowIndexer = new ArrayList<>(); 
		
		while ((line = br.readLine()) != null) {
			StringIntegerPair temp = new StringIntegerPair();
			List<String> list  =Arrays.asList(line.split(","));
			temp.setIndex(Integer.parseInt(list.get(0)));
			temp.setName(list.get(1));
			fileRowIndexer.add(temp);
		}
		//System.out.println(fileRowIndexer.get(0).getName());
		String ResultPath = "C:\\Users\\tongy\\Desktop\\CS172\\project\\CS172_Project\\Part A";
		PrintWriter writer = new PrintWriter(fileName);

		

		String indexDir = "C:\\Users\\tongy\\Desktop\\ttt";
		Analyzer analyzer = new StandardAnalyzer();
		Directory directory =FSDirectory.open(FileSystems.getDefault().getPath(indexDir));
		DirectoryReader indexReader= DirectoryReader.open(directory);
		IndexSearcher indexSearcher =new IndexSearcher(indexReader);
		QueryParser parser = new QueryParser("content",analyzer);

		Query query = parser.parse(querystr);
		System.out.println("seeking query : " + query);
		int topHitCount =100;
		ScoreDoc[] hits = indexSearcher.search(query,topHitCount).scoreDocs;
		System.out.println("num of hits: " + hits.length);
		StringBuilder colNames = new StringBuilder();
		
			colNames.append("fileName");
			colNames.append(',');
			colNames.append("rowID");
			colNames.append(',');
			colNames.append("docID");
			colNames.append(',');
			colNames.append("score");
			colNames.append(',');
			colNames.append("url");
			colNames.append(',');
			colNames.append("title");
			colNames.append(',');
			colNames.append("snippet");
			colNames.append(',');
			colNames.append('\n');
			writer.write(colNames.toString());
		for(int rank=0;rank<hits.length;++rank) {
			Document hitDoc = indexSearcher.doc(hits[rank].doc);
			StringBuilder sb = new StringBuilder();
			
			int docID = hits[rank].doc;
			String docFileName = "";
			
			//get filename and row 
			for(int i= 0;i<fileRowIndexer.size();i++) {
				if(fileRowIndexer.get(i).getIndex() <= docID) {
					docID -= fileRowIndexer.get(i).getIndex();
					
				}
				else {
					docFileName =fileRowIndexer.get(i).getName();
					break;
				}
			}
			
			//get html content for frontend
			String htmlDataFile = "DataFiles\\" + docFileName;
			//System.out.println("dd " + htmlDataFile);
			BufferedReader htmlbr = new BufferedReader(new FileReader(htmlDataFile));
			String row = "";
			sb.append(docFileName);
			sb.append(',');
			sb.append(docID);
			sb.append(',');
			sb.append(hits[rank].doc);
			sb.append(',');
			sb.append(hits[rank].score);
			sb.append(',');
			System.out.println("current " + docFileName + " id: "+ docID );
			row = htmlbr.readLine();
			for(int i = 1; i < docID; ++i) {
				  row = "";
				  row = htmlbr.readLine();
			
			}
				List<String> list  =Arrays.asList(row.split(","));
				String title = list.get(0);
				String url = list.get(1);
				String body = list.get(2);
				int loc = body.toLowerCase().indexOf(querystr);
				String snippet="";
				if (loc > -1 ) {
					int end = loc +100;
					if(body.length()<loc +100) end = body.length()-1;
					snippet = body.substring(loc,end);
				}
				else snippet = body;
				
				//System.out.println("data url " + url);
				
				sb.append(url);
				sb.append(',');
				sb.append(title);
				sb.append(',');
				sb.append(snippet);
				sb.append(',');
			
			sb.append('\n');
			
			
			
			writer.write(sb.toString());
			//System.out.println((rank+1)+" docid: "+ hits[rank].doc +" (score:" +hits[rank].score +") -->"+hitDoc.get("content"));
			//System.out.println(docFileName);
			}
			writer.close();
			indexReader.close();
			directory.close();
			//tester= false;
	}
	
	

	}


}