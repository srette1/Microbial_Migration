class MonaPathParse():
    
    def  __init__(self, input_file_path):
        self._input_file_path = input_file_path
        
    
    def read(self):
        
        path = (self._input_file_path)
        
        path_dict = dict()

        # Break the path variable into a set of folder names
        folders = path.split('/')

        path_dict['Species'],path_dict['Collection Date'] = folders[5].split('_')
        path_dict['Media'] = folders[6].split('_')[1]
        path_dict['Timepoint'], path_dict['Time_Units'] = folders[7].split('_')
        path_dict['Filename'] = folders[8]
        
        if folders[-1].find('_') > 0:
            path_dict['Microfluidic Channel Number'] = folders[8].split('_')[1]
            path_dict['Channel Location'] = folders[8].split('_')[2].split('.')[0]
            
        else:
            path_dict['Microfluidic Channel Number'] = 'not defined'
            path_dict['Channel Location'] = folders[8].split('.')[0]
        
        return path_dict
    