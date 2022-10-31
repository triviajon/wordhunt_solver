# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:29:04 2022

@author: jon-f
"""
import os
import json

common_words_filename = os.path.join(os.getcwd(), 'dictionary_1.txt')
dictionary_filename = os.path.join(os.getcwd(), 'dictionary_2.json')

all_known_words = set()

with open(common_words_filename, 'r') as file:
    common_words = file.read().split('\n')
    all_known_words.update(common_words)
    common_words = set(common_words)

with open(dictionary_filename, 'r') as file:
    dictionary = json.load(file)
    all_known_words.update(dictionary.keys())

class WordHunt:
    def __init__(self, letters, size=4):
        assert len(letters) == size**2, ValueError(f"letters size {len(letters)} != size ({size**2})")
        self.letters = letters
        self.board = [[letters[i+j*size] for i in range(size)] for j in range(size)]
        self.graph = {}
        self.size = size
        
        for i in range(size):
            for j in range(size):

                adj = [(i+dx, j+dy) for dx in range(-1, 2) for dy in range(-1, 2) if not (dx == 0 and dy == 0)]
                adj = [(ip, jp) for ip, jp in adj if (0<=ip<size) and (0<=jp<size)]
                
                self.graph[i, j] = adj

    def __str__(self):
        return self._tostr(self.board)
    
    def _tostr(self, board):
        string_repr = ''
        for line in board:
            line_repr = ' '.join(line)
            string_repr += line_repr + '\n'
        return string_repr

    def __repr__(self):
        return f'WordHunt({self.letters}, size={self.size})'
    
    def print_path(self, path):
        edited_board = [line.copy() for line in self.board]
        
        for i, coords in enumerate(path):
            x, y = coords
            edited_board[x][y] = str(i)
        
        return self._tostr(edited_board)
        
                
    
def order_of_attack(wh):
    # return words in order of most theoretical points
    best_ordering = 'scpdbramtfiehgluwonvjkqyzx'
    
    graph_ordering = []
    
    for i, j in wh.graph.keys():
        corresponding_letter = wh.board[i][j]
        letter_rank = 26 - best_ordering.index(corresponding_letter)
        graph_ordering.append(((i, j), letter_rank))
        
    graph_ordering.sort(key=lambda pair: pair[1], reverse=True)
    return graph_ordering

def find_words(wh, stop_after=5, min_distance=3):
    # given a  graph, get paths of length between min_distance and stop_after
    # to do: use a better distance metric than manhatten_distance
    graph = wh.graph
    graphletters = wh.board
    all_words = []
    attack_order = order_of_attack(wh)
    
    for i, pair in enumerate(attack_order):
        start, _ = pair
        end_ordering = [(k, manhatten_distance(start, k)) for k in graph.keys()]
        end_ordering.sort(key=lambda pair: pair[1], reverse=True)
        
        for end, _ in end_ordering:
            if start == end or manhatten_distance(start, end)<min_distance or \
                i >= stop_after: continue
            
            paths = find_all_paths(graph, start, end)
        
            for path in paths:
                jargan = ''.join([graphletters[i][j] for i, j in path])
                if jargan in all_known_words: 
                    all_words.append((jargan, path))
            
    return sorted(all_words, key=lambda p: len(p[0]), reverse=True)

def give_words(words, wh, at_once=4):
    
    ix = 0
    while ix < len(words):        

        for word, coords in words[ix:ix+at_once]:
            print(word)
            print(wh.print_path(coords))
        cont = input("Would you like to continue (press any key for yes, or type no/quit for no): ")
        
        ix += at_once
        if cont.lower() in {'n', 'no', 'quit'}:
            break

def manhatten_distance(x, y):
    return sum([abs(x[0]-y[0]), abs(x[1]-y[1])])
        
def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths   

if __name__ == "__main__":
    game_letters = input("What are the game letters (in order, no spaces): ").lower()
    game = WordHunt(list(game_letters))
    all_words = find_words(game)
    give_words(all_words, game)