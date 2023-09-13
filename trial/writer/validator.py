    async def validate_bloom_filter_array(self, bf: BloomFilter, initial=False):
        print(f"New Bloom filter hash count: {bf.hash_count}")
        temp_false_elements = np.array([str(random.randint(100000, 300000)) for _ in range(len(bf.bf_array.array)) ])
        true_elements = np.array([ str(item['ID']) for item in self.ids ])

        # Find the set difference between temp_false_elements and true_elements
        false_elements = np.setdiff1d(temp_false_elements, true_elements)

        # Concatenate true_elements and false_elements into combined_elements
        combined_elements = np.concatenate((false_elements,  true_elements))        
        false_negatives = 0
        false_positives = 0
        false_positive_ratio = 0
        true_negatives = 0
        

        # for item in false_elements:
        #     #avoid duplicate with true elements
        #     distinct_val = "pre" + item 
        #     if not bf.check(distinct_val) and distinct_val not in self.ids:
        #         true_negatives += 1

        # for item in false_elements:
        #     if bf.check(item): #this makes it unique and not in the true elements
        #         false_positives += 1

        # for item in combined_elements:
        #     if not bf.check(item):
        #         if item not in true_elements:
        #             true_negatives += 1
        #         else:
        #             print(item)

        #     else:
        #         if item not in true_elements:
        #             false_positives += 1
        
        isDuplicate = False
        for item in false_elements:
            if item in true_elements:
                isDuplicate = True


        for item in combined_elements:
            if not bf.check(item):
                if item in true_elements:
                    false_negatives += 1

            else:
                if item not in true_elements:
                    false_positives += 1


        false_positive_ratio = false_positives / len(combined_elements)
        false_negatives_ratio = false_negatives / len(combined_elements)
        true_negatives_ratio = true_negatives / len(combined_elements)
        print(f"Is dup: {isDuplicate} Initial test: {initial} false positives ratio: {false_positive_ratio} FN: {false_negatives} TE size: {len(true_elements)},{len(false_elements)},#true negatives {true_negatives}")
        # print(f"false_negatives ratio: {false_negatives_ratio}, {false_negatives}, {len(false_elements)}")
        print(f"true negatives ratio: {true_negatives_ratio}")        
