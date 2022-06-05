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


import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
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
import java.io.FileWriter;
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
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;


/** Index all text files under a directory.
 * <p>
 * This is a command-line application demonstrating simple Lucene indexing.
 * Run it with no command-line arguments for usage information.
 */




public class HTMLFilesIndexer {

public static void main(String[] args) throws IOException,ParseException
{   
	
	String ResultPath = "C:\\Users\\tongy\\Desktop\\CS172\\project\\CS172_Project\\Part A";
	PrintWriter writer = new PrintWriter("fileRowIndexer.csv");
	



	String indexDir = "C:\\Users\\tongy\\Desktop\\ttt";
	Analyzer analyzer = new StandardAnalyzer();
	Directory directory =FSDirectory.open(FileSystems.getDefault().getPath(indexDir));
	


	int count = 0;
	String dataPath = "C:\\Users\\tongy\\Desktop\\CS172\\project\\CS172_Project\\Part A\\DataFiles";
	File folder = new File(dataPath);
	File[] listOfFiles = folder.listFiles();
	
	for (File edu : listOfFiles) {
		if (edu.isFile()) {
			
			String perCSVFile = dataPath+"\\"+edu.getName();
			System.out.println("edu csv: "+perCSVFile);
			IndexWriterConfig config = new IndexWriterConfig(analyzer);
			IndexWriter indexWriter = new IndexWriter(directory, config);
			ArrayList<String> content = new ArrayList<String>();
			BufferedReader br = new BufferedReader(new FileReader(perCSVFile));
			String line = "";
			while ((line = br.readLine()) != null) {
				List<String> list  =Arrays.asList(line.split(","));
				String title = list.get(0);
				String url = list.get(1);
				String body = list.get(2);

				content.add((title + " "+body));
			}

			String[] singleEdu = content.toArray(new String[0]);

			System.out.println("num doc: "+singleEdu.length);
			StringBuilder sb = new StringBuilder();

			sb.append(singleEdu.length);
			sb.append(',');
			sb.append(edu.getName());
			sb.append('\n');

			writer.write(sb.toString());
			
			for (String page:singleEdu) {
				Document doc = new Document();
				doc.add(new Field("content",page,TextField.TYPE_STORED));
				indexWriter.addDocument(doc);
			}
			indexWriter.close();
		}
		
	}
	writer.close();

}
}