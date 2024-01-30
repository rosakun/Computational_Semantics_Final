import os
import openai
import json
openai.api_key = "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"

# Use a model from OpenAI (assuming "text-embedding-ada-002" exists for this example)
model_name="gpt-3.5-turbo-instruct"

def maria_prompt(drg):

    drg = "\n".join(drg)

    example_broken_drg = "\n".join([ 
    "person.n.01     EQU speaker                     % I was     [0-5]",
    "search.v.01     Agent -1 Theme +2 Destination +3 % searching [6-15]",
    "full.a.01      AttributeOf +1                    % some full         [16-25]",
    "movie.n.01                                      % movies in         [26-35]",
    "youtube.n.01                                    % youtube, and      [36-48]",
    "           CONTINUATION <1                  %",                   
    "some.n.01                                        % some are          [49-57]",
    "remove.v.01    Theme -1 Instrument +1            % removed by        [58-68]",
    "youtube.n.01                                    % youtube,          [69-77]"])

    example_fixed_drg = "\n".join([ 
    "person.n.01     EQU speaker                     % I was     [0-5]",
    "search.v.01     Agent -1 Theme +2 Destination +3 % searching [6-15]",
    "full.a.01      AttributeOf +1                    % some full         [16-25]",
    "movie.n.01                                      % movies in         [26-35]",
    "youtube.n.01                                    % youtube, and      [36-48]",
    "           CONTINUATION <1                  %",                   
    "movie.n.01                                        % some are          [49-57]",
    "remove.v.01    Theme -1 Instrument +1           % removed by        [58-68]",
    "youtube.n.01                                    % youtube,          [69-77]"])

    prompt_text = "Let's think step by step. The ellipsis is introduced by the word 'some'.  In the sentence, 'some' refers to 'movies'. We do not replace 'some' with 'movie'. The WordNet sense corresponding to the word 'some' is 'some.n.01'.  The WordNet sense corresponding to 'movies' is 'movie.n.01'. So, we replace 'some.n.01' with 'movie.n.01'." 

    lets_think = "Let's think step by step."

    full_prompt = "Q:\n" + example_broken_drg + "\n\n" + prompt_text + "\n\n" + "A:\n" + example_fixed_drg + "\n\n" + "Q:\n" + drg + "\n\n" + lets_think

    return full_prompt 

def renee_prompt(drg,sentence,shots=5):

    drg = "\n".join(drg)

    preface_text = "Below are five examples of a discourse representation graph (DRG) with an incorrectly annotated noun ellipsis and their corrected versions. First a sentence is shown, then the DRG with the incorrectly annoted noun ellipsis for that sentence, and the the DRG with the correctly annotated noun ellipsis.\n\n"
    incorrect_drg = "Incorrect DRG:\n"
    correct_drg = "Correct DRG:\n"
    postface_text = "Please give a DRG with a correctly annotated noun ellipsis as correct DRG given the following sentence and incorrect DRG.\n\nSentence: "
    sentence_1 = "Sentence: I was searching some full movies in youtube, and some are removed by youtube.\n"
    incorrect_drg_1 = "\n".join(["person.n.01    EQU speaker                      % I was    ",         
                    "search.v.01    Agent -1 Theme +2 Destination +3 % searching         ",
                    "full.a.01      AttributeOf +1                   % some full         ",
                    "movie.n.01                                      % movies in         ",
                    "youtube.n.01                                    % youtube, and      ",
                    "CONTINUATION <1                  %                   ",
                    "some.n.01                                       % some are         ",
                    "remove.v.01    Theme -1 Instrument +1           % removed by        ",
                    "youtube.n.01                                    % youtube"])
    correct_drg_1 = "\n".join(["person.n.01    EQU speaker                      % I was       ",      
                    "search.v.01    Agent -1 Theme +2 Destination +3 % searching      ",   
                    "full.a.01      AttributeOf +1                   % some full        ", 
                    "movie.n.01                                      % movies in         ",
                    "youtube.n.01                                    % youtube, and      ",
                    "CONTINUATION <1                  %     ",
                    "full.a.01      AttributeOf +1         % some are ",
                    "movie.n.01       ",
                    "remove.v.01    Theme -1 Instrument +1           % removed by        ",
                    "youtube.n.01                                    % youtube"
    ])
    sentence_2 = "Sentence: If you need an umbrella I'll lend you one.\n"
    incorrect_drg_2 = "\n".join([
                    "person.n.01   EQU hearer                             % If you      [0-6]",
                    "need.v.02     Pivot -1 Time +1 Theme +2              % need        [7-11]",
                    "time.n.08     EQU now                                %             ",
                    "umbrella.n.01                                        % an umbrella [12-23]",
                    "CONSEQUENCE <1                         %             ",
                    "person.n.01   EQU speaker                            % I           [24-25]",
                    "time.n.08     TSU now                                % 'll         [25-28]",
                    "lend.v.02     Agent -2 Time -1 Recipient +1 Theme +2 % lend        [29-33]",
                    "person.n.01   EQU hearer                             % you         [34-37]",
                    "one.n.01                                        % one.        [38-42]"
    ])
    correct_drg_2 = "\n".join([
                    "person.n.01   EQU hearer                             % If you      [0-6]",
                    "need.v.02     Pivot -1 Time +1 Theme +2              % need        [7-11]",
                    "time.n.08     EQU now                                %             ",
                    "umbrella.n.01                                        % an umbrella [12-23]",
                    "CONSEQUENCE <1                         %             ",
                    "person.n.01   EQU speaker                            % I           [24-25]",
                    "time.n.08     TSU now                                % 'll         [25-28]",
                    "lend.v.02     Agent -2 Time -1 Recipient +1 Theme +2 % lend        [29-33]",
                    "person.n.01   EQU hearer                             % you         [34-37]",
                    "umbrella.n.01                                        % one.        [38-42]"
    ])
    sentence_3 = "Sentence: What color is your underwear? I'm not wearing any.\n"
    incorrect_drg_3 = "\n".join(["event.v.01     Participant +1               %             ",
                    "color.n.01                                  % What color [0-11]",
                    "be.v.01        Theme -1 Time +1 Co-Theme +3 % is          [12-14]",
                    "time.n.08      EQU now                      %             ",
                    "person.n.01    EQU hearer                   % your        [15-19]",
                    "underwear.n.01 User -1                      % underwear? [20-31]",
                    "CONTINUATION <1              %             ",
                    "person.n.01    EQU speaker                  % I          [32-34]",
                    "NEGATION <1                  %             ",
                    "time.n.08      EQU now                      % 'm not      [34-40]",
                    "wear.v.01      Agent -2 Time -1 Theme +1    % wearing     [41-48]",
                    "any.n.01                                    % any.       [49-54]"])
    correct_drg_3 = "\n".join([
                    "event.v.01     Participant +1               %             ",
                    "color.n.01                                  % What color [0-11]",
                    "be.v.01        Theme -1 Time +1 Co-Theme +3 % is          [12-14]",
                    "time.n.08      EQU now                      %             ",
                    "person.n.01    EQU hearer                   % your        [15-19]",
                    "underwear.n.01 User -1                      % underwear? [20-31]",
                    "CONTINUATION <1              %             ",
                    "person.n.01    EQU speaker                  % I          [32-34]",
                    "NEGATION <1                  %             ",
                    "time.n.08      EQU now                      % 'm not      [34-40]",
                    "wear.v.01      Agent -2 Time -1 Theme +1    % wearing     [41-48]",
                    "underwear.n.01                                    % any.       [49-54]",
    ])
    sentence_4 = "Sentence: The police cracked down on young people and took hundreds into custody. Several died, apparently from beatings.\n"
    incorrect_drg_4 = "\n".join(["police.n.01                                               % police        [894-900]",
                    "crack.v.01       Theme -1 Time +1 Path +2                  % cracked       [901-908]",
                    "time.n.08        TPR now                                   %    ",
                    "entity.n.01      Theme +2                                  % down on       [909-916]",
                    "young.a.01       AttributeOf +1                            % young         [917-922]",
                    "person.n.01                                                % people and    [923-933]",
                    "take.v.01        Agent -6 Time +1 Theme +2 Destination +3  % took          [934-938]",
                    "time.n.08        TPR now                                   %            ",
                    "measure.n.02     Quantity 200                              % hundreds into [939-952]",
                    "custody.n.01                                               % custody.      [953-961]",
                    "CONTINUATION <1  ",
                    "measure.n.02     Quantity +                                % Several       [963-970]",
                    "die.v.01         Patient -1 Time +1 Manner +2 Source +3    % died,         [971-976]",
                    "time.n.08        TPR now                                   %     ", 
                    "apparently.a.01                                            % apparently from [977-992]",
                    "beating.n.01                                               % beatings.      [993-1002]",
    ])
    correct_drg_4 = "\n".join(["police.n.01                               % police                  [894-900]",
                    "crack.v.01      Theme -1 Time +1 Path +2   % cracked                 [901-908]",
                    "time.n.08       TPR now                    %   ",
                    "entity.n.01     Theme +2                   % down on                 [909-916]",
                    "young.a.01      AttributeOf +1             % young                   [917-922]",
                    "person.n.01                                % people and              [923-933]",
                    "take.v.01       Agent -6 Time +1 Theme +2 Destination +3    % took   [934-938]",
                    "time.n.08       TPR now                    %   ",
                    "measure.n.02    Quantity 200               % hundreds into            [939-952]",
                    "custody.n.01                               % custody.                 [953-961]",
                    "CONTINUATION <1                            %                           ",
                    "young.a.01       AttributeOf +1            % Several                  [917-922]",
                    "person.n.01        ",
                    "die.v.01         Patient -1 Time +1 Manner +2 Source +3   % died,     [971-976]",
                    "time.n.08        TPR now                   %    ",
                    "apparently.a.01                            % apparently from          [977-992]",
                    "beating.n.01                               % beatings."])
    sentence_5 = "Sentence: Why is the challenge of education unmet in so many countries? Some are simply too poor to provide decent schools.\n"
    incorrect_drg_5 = "\n".join(["reason.n.01    Name ?              % Why",                                                                                             
                    "be.v.01           Location -1 Time +1 Co-Theme +2 Theme +4 Location +5 % is",                                                                                              
                    "time.n.08         EQU now             %  ",                                                           
                    "challenge.n.01    PartOf +1           % the challenge of   ",
                    "education.n.01                        % education         ",
                    "unmet.n.01                            % unmet in          ",
                    "so.r.01           Quantity ?          % so many           ",
                    "country.n.01      EQU -1              % countries?        ",
                    "CONTINUATION <1         %                                 ",
                    "some.n.01                             % Some              ",
                    "time.n.08         EQU now             % are               ",
                    "simply.a.01                           % simply            ",
                    "too.r.01                              % too              ",
                    "poor.a.01         Time -3 Manner -2 Agent -4 Degree -1 Topic +1     % poor to ",
                    "provide.v.01      Agent -5 Theme +2   % provide       ",
                    "decent.a.01       AttributeOf +1      % decent         ",
                    "school.n.01                           % schools.",
    ])
    correct_drg_5 = "\n".join(["reason.n.01     Name ?       % Why",
                    "be.v.01          Location -1 Time +1 Co-Theme +2 Theme +4 Location +5 % is",
                    "time.n.08        EQU now      %",
                    "challenge.n.01   PartOf +1     % the challenge of",
                    "education.n.01                % education",
                    "unmet.n.01                    % unmet in",
                    "so.r.01          Quantity ?   % so many",
                    "country.n.01     EQU -1       % countries?",
                    "CONTINUATION <1               %",
                    "country.n.01                  % Some",
                    "time.n.08        EQU now      % are",
                    "simply.a.01                   % simply",
                    "too.r.01                      % too",
                    "poor.a.01        Time -3 Manner -2 Agent -4 Degree -1 Topic +1     % poor to",
                    "provide.v.01     Agent -5 Theme +2   % provide",
                    "decent.a.01      AttributeOf +1      % decent",
                    "school.n.01                          % schools."
    ])
    if shots == 5:
        full_prompt = preface_text + sentence_1 + incorrect_drg + incorrect_drg_1 + "\n" + correct_drg + correct_drg_1 + "\n\n" + sentence_2 + incorrect_drg + incorrect_drg_2 + "\n" + correct_drg + correct_drg_2 + "\n\n" + sentence_3 + incorrect_drg + incorrect_drg_3 + "\n" + correct_drg + correct_drg_3 + "\n\n"+ sentence_4 + incorrect_drg + incorrect_drg_4 + "\n" + correct_drg + correct_drg_4 + "\n\n" + sentence_5 + incorrect_drg + incorrect_drg_5 + "\n" + correct_drg + correct_drg_5 + "\n\n" + postface_text + sentence + "\n" + incorrect_drg + drg + "\n" + correct_drg
    
    return full_prompt

def sal_prompt(drg):

    drg = "\n".join(drg)
    preface_text = "I will show you a discourse representation graph that contains a incorrectly annotated noun ellipsis. The annotation makes use of WordNet synsets. You are supposed to resolve this incorrectly annotated noun ellipsis by giving the right WordNet synset. Please only respond with the corrected discourse representation graph without any explanation. Iam correcting noun pharse ellipsis only and nothing else should be affected by the correction."

    full_prompt = preface_text + "\n\n" + drg

    return full_prompt


def chat_with_openai(prompt,temperature=0,top_p=1):
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    max_tokens=350,
    temperature=temperature,
    top_p=top_p
    )

    # Print the generated function
    return response.choices[0].text



def test_single_example():
    """
    I used this function to test my chat_with_openai script on the first example of the dev set.
    """
    with open('devSet.json', 'r') as json_file:
        json_obj = json.load(json_file)
        first_drg = json_obj[0]['drg']
        first_sentence = json_obj[0]['sentence']
        first_prompt = sal_prompt(first_drg)

        print(chat_with_openai(first_prompt,temperature=0))


def return_drg(drg,sentence,user='maria'):
    """
    Takes a DRG as input, passes it to GPT, and returns the (hopefully) corrected output DRG.
    """
    if user=='maria':
        prompt = maria_prompt(drg)
        response = chat_with_openai(prompt)
        try:
            output_drg = response.split("A:")[1]
            return output_drg
        except IndexError:
            return response
    elif user=='renee':
        prompt = renee_prompt(drg,sentence)
        response = chat_with_openai(prompt)
        return response
    elif user=='sal':
        prompt = sal_prompt(drg)
        response = chat_with_openai(prompt)
        return response


def evaluate_on_testset():
    output_drgs = []
    with open('testSet.json','r',encoding='utf-8') as test_set:
        for json_item in json.load(test_set):
            sentence = json_item['sentence']
            input_drg = json_item['drg']
            output_drg = return_drg(input_drg,sentence,user='renee').split("\n")

            output_drgs.append({
                'sentence': sentence,
                'drg': output_drg
            })
    with open('testSet_outputs_Renee_Temp_0.json','w',encoding='utf-8') as output_file:
        json.dump(output_drgs,output_file,indent=4)



if __name__ == "__main__":
    #test_single_example()
    evaluate_on_testset()