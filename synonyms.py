import math
import time

def norm(vec):
    sum = 0
    for i in vec:
        sum += vec[i] ** 2
    
    return math.sqrt(sum)


def cosine_similarity(vec1, vec2):
    product_sim = 0

    if len(vec1) == 0 or len(vec2) == 0:
        return - 1
    else:
        for i in vec1:
            if i in vec2:
                product_sim += vec1[i] * vec2[i]
        
    return product_sim / (norm(vec1) * norm(vec2))
        

#print(cosine_similarity({"a": 1, "b": 2, "c":3}, {"b": 4, "c":5, "d":6}))


def build_semantic_descriptors(sentences):
    descriptors = {} 


    for sentence in sentences:
        for word in sentence:
            word = word.lower()
            if word == '':
                continue
            if word in descriptors:
                pass
            else:
                descriptors[word] = {}
            word_dict = descriptors[word]
            for word_two in sentence:
                word_two = word_two.lower()
                if word_two == word or word_two == '':
                    continue 
                else:
                    if word_two in word_dict:
                        word_dict[word_two] += 1
                    else:
                        word_dict[word_two] = 1
        
    #print(descriptors['man'])
    #print(descriptors['liver'])
    
    return descriptors
            


            
    
    

'''build_semantic_descriptors([["i", "am", "a", "sick", "man"],
["i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]])'''

def combine_text(files):
    str=''
    for file in files:
        file_data = open(file, 'r', encoding='latin1')
        content = file_data.read()
        str += content 
    return str


def build_semantic_descriptors_from_files(filenames):
    combined_txt = combine_text(filenames)

    
    new_content = combined_txt.replace('?', '.')
    new_content_exclamation = new_content.replace('!', '.')
    new_content_exclamation_dash = new_content_exclamation.replace('-', '.')
    
     # to take into consideration the possibility the end of a phrase
    array = new_content_exclamation_dash.split('.')
    text_array = []
    for sentence in array:
        sentence_array = sentence.split(' ')
        text_array.append(sentence_array)


        
    #print(text_array)
    file_descriptor_result_from_func = build_semantic_descriptors(text_array)
    return file_descriptor_result_from_func
        
            
#print(build_semantic_descriptors_from_files(['test.txt']))

def sort_dict_values(dict):
    values = sorted(dict.values(), reverse=True)
    max_val = values[0]
    for key in list(dict.keys()):
        if dict[key] == max_val:
            return key 
        else:
            continue




def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    word_to_sim_dict = {} 
    try:
        word_vec = semantic_descriptors[word] #word vec

        for word in choices:
            word_choice_vec = semantic_descriptors[word] #word choice vec
            cosine_similarity = similarity_fn(word_vec, word_choice_vec)
            word_to_sim_dict[word] = cosine_similarity

        dict_sorted = sort_dict_values(word_to_sim_dict)
        return dict_sorted
    except:
        return -1
    



def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    file = open(filename, 'r', encoding='latin1')
    content = file.read().split('\n')
    total = len(content)
    count = 0
    for phrase in content:
        
        if phrase == '':
            continue
        formatted_phrase = phrase.split(' ')
        desired_word = formatted_phrase[0]
        answer = formatted_phrase[1]
        choices = formatted_phrase[2:len(phrase)]
        
            
        cosine_sim_dict_result = most_similar_word(desired_word, choices, semantic_descriptors, similarity_fn)

        if cosine_sim_dict_result == answer:
            print("Correct: ", phrase)
            count += 1
            
            
    
    return (count / total) * 100


'''current_time = time.time()
sem_descriptors = build_semantic_descriptors_from_files(["sw.txt", "wp.txt"])
res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
print(res, "of the guesses were correct")
after_time = time.time()
print("Time taken (s): ", after_time - current_time)'''
