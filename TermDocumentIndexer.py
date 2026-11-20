# Group 9: Akira Doi, Dylan Garvey
# Professor Malik Luti
# CECS 429 Sec02
# 11/21/2026

from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, TermDocumentIndex
from text import BasicTokenProcessor, EnglishTokenStream

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def index_corpus(corpus : DocumentCorpus) -> Index:
    
    token_processor = BasicTokenProcessor()
    vocabulary = set()
    
    for d in corpus:
        print(f"Found document {d.title}")
        # TODO:
        #   Tokenize the document's content by creating an EnglishTokenStream around the document's .content()
        #   Iterate through the token stream, processing each with token_processor's process_token method.
        #   Add the processed token (a "term") to the vocabulary set.

        # Make the document text into token
        # Iterate through the token stream
        for token in EnglishTokenStream(d.get_content()):
            # Normalize the token (removes all non-alphanumeric characters and lowercases a token)
            term = token_processor.process_token(token)
            # Skip the empty instead of printing empty term
            if term != "":
                vocabulary.add(term)

    # TODO:
    # After the above, next:
    # Create a TermDocumentIndex object, with the vocabular you found, and the len() of the corpus.
    # Iterate through the documents in the corpus:
    #   Tokenize each document's content, again.
    #   Process each token.
    #   Add each processed term to the index with .add_term().

    # Create index for the TermDocumentIndex object
    index = TermDocumentIndex(vocabulary, len(corpus))
    for d in corpus:
        for token in EnglishTokenStream(d.get_content()):
            term = token_processor.process_token(token)
            if term != "":
                index.add_term(term, d.id)
    # Return the index
    return index


if __name__ == "__main__":
    # Create path for the "Moby Dick" folder, this folder in the "Group9_Assignment4" 
    # so use .parent.parent to check "Group9_Assignment4" that is saved "Moby Dick" folder from this
    corpus_path = Path(__file__).resolve().parent.parent / "Moby Dick"
    d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")

    # Build the index over this directory.
    index = index_corpus(d)

    # -- Find "whale" with Hard Code --
    # query = "whale" # hard-coded search for "whale"
    # for p in index.get_postings(query):
    #    print(f"Document {d.get_document(p.doc_id)}")

    # Prepared processor to allow normalization for the query
    processor = BasicTokenProcessor()

    # Expand the app so that the user is prompted for a term to search for.
    # (Loop the main until the user enters "quit".)
    while True:
        userQuery = input("Enter a term to search for. (You can exit by entering 'quit') : ")

        # user exit with 'quit'
        if userQuery.lower() == "quit":
            break

        # Normalize the query
        term = processor.process_token(userQuery)
        # Get that postings (document ID)
        postings = index.get_postings(term)

        # If no document in the 'Moby Dick' has that term
        if not postings:
            print("The entered term is not exist in these documents.")

        # If found entered term, return it
        for p in postings:
            print(f"Document {d.get_document(p.doc_id)}")
