# rags are used to help the llm to get data from external sources like files or databases
# rags basically doesn't search for exact words but for similar meaning
# for this first files are divided into number of chunks (all equal sizes) of token size of your choice
#tokens are the units of chunks it can be a character or a word
# after creating chunks, these are embedded into vector representation
# database "vector db" is used to store these vectors
# when user sends the prompt , the "retrival" will reterive chunks with meaning same as prompt and return it to the llm


