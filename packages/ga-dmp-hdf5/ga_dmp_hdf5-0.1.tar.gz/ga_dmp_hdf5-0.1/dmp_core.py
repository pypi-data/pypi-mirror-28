#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import numpy
import h5py
import re
import os

from collections import OrderedDict
# Issues array with everything
# Issues dict with classifications for the issues.  IE issues[figure_number]

defaults = {}
defaults['file_path'] = "./"
defaults['doc_number'] = "AXXXXX"
defaults['author'] = "author"
defaults['data_provider'] = "provider"
defaults['journal'] = "journal"
defaults['year'] = "XXXX"
defaults['figure_number'] = "XX"
defaults['citation'] = "X"

def urlify(s):
    # Allow letters, numbers and dashes ('-')
    s = re.sub(r"[^\w\s-]", '', s)
    
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)
    return s
    
def sanitize(s):
    # Allow letters, numbers and dashes ('-')
    s = re.sub(r"[^\w\s-]", '', s)
    
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)
    
    # remove underscores
    s = re.sub(r"_", '-', s)
    return s



def make_file_name(author, journal, year, figure):
    '''   
    Takes meta-data information and returns an 
    appropriate file name for dmp submission.
    All parameters are required.
    
    author          : The first author of the publication
    journal         : Journal this publication appears in.
    year            : The year this publication appears in a journal.
    figure          : The figure number for this data.  
                        (Does NOT need to be prefixed with "Fig")
    '''
    journal = sanitize(journal)
    file_name = "DIII-D_"+author+"_"+journal+"_"+year+"_"+"Fig"+figure
    file_name = urlify(file_name)
    file_name = file_name + ".h5"
    return file_name
 
class DMPCore(object):
    
    def __init__(self,
                data = [], 
                file_path = defaults['file_path'], 
                doc_number = defaults['doc_number'],
                author = defaults['author'],
                data_provider = defaults['data_provider'], 
                journal = defaults['journal'], 
                year = defaults['year'], 
                figure_number = defaults['figure_number'], 
                citation = defaults['citation']):
        
        self.meta = {}
        self.data = []
        self.open_hdf5 = None
        self.issues = []
        self.warnings = []
        self.disk_file_name = ""
        self.disk_full_file_path = "./"
           
        self.meta['file_path'] = file_path
        self.meta['doc_number'] = doc_number
        self.meta['author'] = author
        self.meta['data_provider'] = data_provider
        self.meta['journal'] = journal
        self.meta['year'] = year
        self.meta['figure_number'] = figure_number
        self.meta['citation'] = citation
        self.data = data    

    def __del__(self):
        if self.open_hdf5 != None:
            self.open_hdf5.close()

    # Properties
    
    # file path
    def get_file_path(self):
        return self.meta['file_path']
    def set_file_path(self, value):
        self.meta['file_path'] = value
    file_path = property(get_file_path, set_file_path)
    
    # doc number
    def get_doc_number(self):
        return self.meta['doc_number']
    def set_doc_number(self, value):
        self.meta['doc_number'] = value
    doc_number = property(get_doc_number, set_doc_number)
    
    # author
    def get_author(self):
        return self.meta['author']
    def set_author(self, value):
        self.meta['author'] = value
    author = property(get_author, set_author)
    
    # data provider
    def get_data_provider(self):
        return self.meta['data_provider']
    def set_data_provider(self, value):
        self.meta['data_provider'] = value
    data_provider = property(get_data_provider, set_data_provider)
    
    # journal 
    def get_journal(self):
        return self.meta['journal']
    def set_journal(self, value):
        self.meta['journal'] = value
    journal = property(get_journal, set_journal)
    
    # year
    def get_year(self):
        return self.meta['year']
    def set_year(self, value):
        self.meta['year'] = value
    year = property(get_year, set_year)
        
    # figure number
    def get_figure_number(self):
        return self.meta['figure_number']
    def set_figure_number(self, value):
        self.meta['figure_number'] = value
    figure_number = property(get_figure_number, set_figure_number)

    # citation
    def get_citation(self):
        return self.meta['citation']
    def set_citation(self, value):
        self.meta['citation'] = value
    citation = property(get_citation, set_citation)
    
    # Use information we know to try and guess other information
    def auto_fill_meta(self):
            
        if "data_provider" not in self.meta.keys() or self.meta['data_provider'] == defaults['data_provider'] or self.meta['data_provider'] == "":
            if "author" in self.meta.keys() and self.meta['author'] != defaults['author']:
                self.meta['data_provider'] = self.meta['author']
        
        if "author" not in self.meta.keys() or self.meta['author'] == defaults['author'] or self.meta['author'] == "":
            if "data_provider" in self.meta.keys() and self.meta['data_provider'] != defaults['data_provider']:
                self.meta['author'] = self.meta['data_provider']
        
            # Try to use the citation to figure out the journal and the year
        if "citation" in self.meta.keys() and self.meta['citation'] != defaults['citation'] and self.meta['citation'] != "":
            #Find the year in the citation
            if "year" not in self.meta:
                self.meta['year'] = defaults['year']
            years = re.findall(r"[0-9][0-9][0-9][0-9]", self.meta['citation'])
            if (len(years) > 0):
                if self.meta['year'] == defaults['year'] or self.meta['year'] == "":
                    # The last thing formatted like a year is most likely to be the correct one.
                    self.meta['year'] = years[-1]
                elif self.meta['year'] != years[-1]:
                    warnings.append("Year provided (" +  self.meta['year'] + ") does not match citation year (" + years[-1] +")")
            
            # I've noticed that when the citation is correct, there is usually a coma in between the journal name & issue number and the rest.
            # the issue number tends to be right before the comma.  We'll use this to try to fill in the journal if it hasn't 
            # been provided
            citation_parts = self.meta['citation'].split(',')
            if len(citation_parts) > 0:
                journal = citation_parts[0]
                # remove the trailing numbers
                journal = re.sub(r"[0-9]+$",'',journal)
                # remove trailing spaces
                journal = re.sub(r"\s+$",'',journal)
                # Since journal is used in file name, need to urlify it.
                journal = sanitize(journal)
                if "journal" not in self.meta or self.meta['journal'] == defaults['journal'] or self.meta['journal'] == "":
                    self.meta['journal'] = journal
                elif self.meta['journal'] != journal:
                    warnings.append("Journal provided (" + self.meta['journal'] + ") does not match citation journal (" + journal + ")")

    def print_formated_meta(self):

        for key, value in self.meta.iteritems():
            if key != "DATA":
                print "\t"+key + "\t:\t" + str(value)
        return 
    
    def get_problem_meta_keys(self):
        #each key should exist, not be blank, not be default, year should have 4 digits
        requiredKeys = ('doc_number', 'data_provider', 'figure_number', 'citation', 'author', 'year', 'journal')
        
        issues = []
        
        for key in requiredKeys:
            if key in self.meta:
                if self.meta[key] == defaults[key]:
                    issues.append(key)
                if self.meta[key] == "":
                    issues.append(key)
            else:
                issues.append(key)
        #year should be formatted with 4 numeric digits
        if 'year' in self.meta and not re.match(r"^[0-9][0-9][0-9][0-9]$", self.meta['year']):
            if 'year' not in issues:
                issues.append('year')
        
        return issues
    
    def verify_file_name(self, file_name):
        '''
        Takes a file name and opens it as an hdf5 file.
        It checks the file name as well as the hdf5 file
        to make sure it would pass submission tests.
        
        Returns an array of issues found with the hdf5 meta-data'''
        
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        terms = base_name.split('_')
        self.issues = []
        #filename should have 5 sections
        num_terms = len(terms)
        if num_terms != 5:
            self.issues.append("File name should have 5 sections each separated by '_', this file has "+  str(num_terms))
        if num_terms >= 1 and terms[0].lower() != "DIII-D".lower():
            self.issues.append("Section 1 of file name ("+ terms[0]+") should be 'DIII-D'");
        if num_terms >= 2 and terms[1].lower() == defaults['author'].lower():
            self.issues.append("Section 2 of file name ("+ terms[1]+") should not be default value")
        if num_terms >= 3 and terms[2].lower() == defaults['journal'].lower():
            self.issues.append("Section 3 of file name ("+ terms[2]+")  should not be default value")
        if num_terms >= 4 and not re.match(r"^[0-9][0-9][0-9][0-9]$", terms[3]):
            self.issues.append("Section 4 of file name ("+ terms[3]+") should be exactly 4 numeric digits")
        if num_terms >= 5 and not re.match(r"^[Ff][iI][gG]", terms[4]):
            self.issues.append("Section 5 of file name ("+ terms[4]+") should begin with 'Fig'")
        if num_terms >= 5 and terms[4].lower() == ("Fig"+defaults['figure_number']).lower():
            self.issues.append("Section 5 of file name ("+ terms[4]+") should not be default value")
        
        i = 0;
        for term in terms:
            i = i + 1
            if term == "":
                self.issues.append("Section " + str(i) + " of the file name should not be blank.")
        return self.issues
    
    
    def verify_meta(self, meta):
        ''' 
        Returns an array of issues found with the meta-data
        '''
    
        self.issues = []    
        requiredKeys = ('doc_number', 'data_provider', 'figure_number', 'citation')
        
        for key in requiredKeys:
            if key in meta:
                if meta[key] == defaults[key]:
                    self.issues.append( key + " should not be default value : "+defaults[key])
                if meta[key] == "":
                    self.issues.append( key + " should not be blank : ")
            else:
                self.issues.append(key + " is missing from hdf5 file")
        return self.issues
    
    def verify_for_dmp(self):
        self.issues = []
        if self.disk_file_name == None:
            self.issues.append("File has not yet been loaded or saved")
        else:
            self.issues = self.issues + self.verify_file_name(self.disk_file_name)
        self.issues = self.issues + self.verify_meta(self.meta)
    
    def make_file_name(self):
        '''   
        Takes meta-data information and returns an 
        appropriate file name for dmp submission.
        All parameters are required.
        
        author          : The first author of the publication
        journal         : Journal this publication appears in.
        year            : The year this publication appears in a journal.
        figure          : The figure number for this data.  
                            (Does NOT need to be prefixed with "Fig")
        '''
        return make_file_name(self.author, self.journal, self.year, self.figure_number)
    
    def get_meta_from_file_name(self, file_name):
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        terms = base_name.split('_')
        num_terms = len(terms)
        
        meta = {}
        if num_terms >= 2 and terms[1] != "":
            meta['author'] = terms[1]
        if num_terms >= 3 and terms[2] != "":
            meta['journal'] = terms[2] 
        if num_terms >= 4 and re.match(r"^[0-9][0-9][0-9][0-9]$", terms[3]):
            meta['year'] = terms[3] 
        if num_terms >= 5 and re.match(r"^[Ff][iI][gG]", terms[4]):
            meta['figure_number'] = terms[4][3:]
        return meta
    
    def get_meta_from_hdf5(self, open_hdf):
        meta = {} 
        for key in open_hdf.keys():
            if key != "DATA" and not isinstance(open_hdf[key], h5py.Group):
                meta[key] = open_hdf[key].value
                # If the creator of this file saved a list into the meta_data fields instead of a single element, 
                # grab it as the first element
                if isinstance(meta[key], list) or isinstance(meta[key],numpy.ndarray):
                    meta[key] = meta[key][0]
        return meta
    
    def load_hdf5(self,full_file_path):
        if self.open_hdf5 != None:
            self.open_hdf5.close()
        try: 
            self.open_hdf5 = h5py.File(full_file_path, 'r+')
        except IOError:
            self.issues.append("Unable to open hdf5 file")
            return
        
        # Load meta
        self.meta.update(self.get_meta_from_file_name(full_file_path))
        self.meta.update(self.get_meta_from_hdf5(self.open_hdf5))
        self.disk_full_file_path = full_file_path
        self.disk_file_name = os.path.splitext(os.path.basename(full_file_path))[0]
        self.file_path = full_file_path
 


    # Takes an open hdf5 file and creates data-sets for any of the required fields not yet existing.
    def create_default_hdf5_meta(self, open_hdf_file):
        dt = h5py.special_dtype(vlen=bytes)
        requiredKeys = ('doc_number', 'data_provider', 'figure_number', 'citation')
        for key in requiredKeys:
            if key not in open_hdf_file.keys():
                new_dataset = open_hdf_file.create_dataset(key, data=(defaults[key].encode('utf8')),dtype=dt)
    
    def update_open_hdf5(self):
        self.create_default_hdf5_meta(self.open_hdf5)
        if "figure_number" in self.meta:
            self.meta["figure_number"] = sanitize(str(self.meta["figure_number"]))
        for key in self.meta.keys():
            if key in self.open_hdf5.keys():
                try:
                    decodeStr = self.meta[key].decode('utf8')
                    
                except UnicodeDecodeError:
                # regular string
                    decodeStr = self.meta[key]
                
                except UnicodeEncodeError:
                    decodeStr = self.meta[key]
                    
                self.open_hdf5[key][...] = (decodeStr.encode('utf8'))
    
    def save_hdf5(self):
        '''    save_hdf5 uses the meta-data to construct an appropriate file name and create an hdf5 
        file with the appropriate fields. 
        
        Only the data parameter is required.  The rest of the named
        parameters are optional strings.
        
        \tdata is a list of header/dataset pairs
        A minimal example with a standard 2 column data set would look like
        [
            [
                'Energy (keV), Normalized Loss', 
                [[ 11.885393  ,   0.        ],[ 12.948636  ,   0.        ],[ 29.259875  ,   0.54834126]]
            ]
        ]
        
        Parameters (All optional) : 
            author          : The first author of the publication
            provider        : The name of the person providing this data. 
                                (Probably you)
            journal         : Journal this publication appears in.
            year            : The year this publication appears in a journal.
            figure          : The figure number for this data.  
                                (Does NOT need to be prefixed with "Fig")
            citation        : The full citation for this publication.
            docnumber       : The GA "A" number assigned to this publication. 
        '''   
    
        # If the file is already loaded, just save the updated meta
        if self.open_hdf5 != None:
            self.update_open_hdf5()
            return
    
        # Try to fill in missing : 
        self.auto_fill_meta()
        dt = h5py.special_dtype(vlen=bytes)
        # Need to encode strings as UTF8 to prevent type conversion issues on some python installs.
        file_name = self.make_file_name(self.meta['author'], self.meta['journal'], self.meta['year'], self.meta['figure_number'])
        full_file_path = self.meta['file_path'] + file_name
        f = h5py.File(full_file_path, 'w')
        doc_number_dataset = f.create_dataset('doc_number', data=(self.meta['doc_number'].encode('utf8')),dtype=dt)
        data_provider_dataset = f.create_dataset('data_provider', data=(self.meta['data_provider'].encode('utf8')), dtype=dt) 
        
        figure_number_dataset = f.create_dataset('figure_number', data=(self.meta['figure_number'].encode('utf8')),dtype=dt)
        figure_number_dataset = f.create_dataset('citation', data=(self.meta['citation'].encode('utf8')),dtype=dt)
        g = f.create_group("DATA")
        for counter, item in enumerate(self.data, start=1):
            dataheader = g.create_dataset('dataheader'+str(counter) , data=(item[0].encode('utf8')))
            dataset = g.create_dataset('dataset'+str(counter), data=item[1])
        f.close()
        self.disk_file_name = file_name
        self.disk_full_file_path = full_file_path
