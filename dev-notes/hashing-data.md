
 ### look into how the SID anonymization works

Look at this old branch that changes test_hash and then delete it. https://github.com/CAHLR/Data-AskOski/compare/update_tests

You accidentally overwrote sidHashBin for a particular timestamp, if Jeff were to restart prod using that timestamp would there be a problem with course histories being incorrect?  probably because I think the anonymization is dependent on some level of randomization... but the seed password is fixed so it shouldn't be random?  yeah it's not random because of `random.seed(seed_pw)` so if prod were to be restarted, there would be no lookup errors with the new sidHashBin

`lookup_dict`: This is the mapping between SID and anonID, which allows user to grab anonymized info for that student.  The lookup table will be stored in /research/UCBD2/edw_data/TIMESTAMP" in the sidHashBin file

In load.py
```
lookup = aes_decrypt(keyword, data_got[0], data_got[1], data_got[2]).decode("utf-8")
lookup_dict = json.loads(lookup)
```

- "biggest pain point is the lookup_dict (anon to SID) because if this is wrong then everything else is wrong in terms of the other lookup tables for majors / courses.  how does the main sid to anon lookup work and how does that affect the course indexing?"

- what is sid_to_hash.txt? (is this the actual lookup file?)  the file is being removed in utils.py
- look at the indexing error action item below

- how to does anon2id lookup (anon2enrollPick.p) work? 
    - anon2enroll is just the anonymous id to enrollment data which uses the lookup_dict to map to the actual student
    - in no-pass mode, anon2enroll uses a `dummy_lookup_dict` to map to fake data student data

- hashed vs encrypted data - which one is the anonymized data using the lookup dict?  Hashed is anonymizing the SID, encrypted data is for the overall files

---

### Task: Indexing error that broke the system for entirety of F19 during the data-askoski transition:

- Service reads from the hashed majors, grades, etc. files which are in the top level of /research/UCBD2/edw_data 

These are older files from the end of summer. It’s decoding the student ids with /research/askoski_common/bins/sidHash_new.bin, which is being overwritten by the data pipeline with mappings calculated from newer data. (are all these things being mapped?)

- Service using old grade, majors, requirements tables + new sid lookup table -> indexing errors
- A really quick fix would be to run the pipeline on old data, which would revert the lookup table and fix the indexing errors on Service.
- I am in the process of pointing the data pipeline to write the lookups to a separate folder that wouldn’t mess with the current Service.

The problem was a combination of a couple issues:

1. some of the file names for campus data dumps were incorrect. not sure who was responsible for this but we should verify file names next time when writing stuff like this.
2. we were loading the ENV json and then rewriting it to disk, but it wasn't being reloaded in memory. we should have sanity checks next time in between stages of the pipeline to check things like this, or better yet, separate out each stage of the pipeline entirely.
3. importing modules caused the ENV json in each one to load at the start meaning it was stale after new json was created. again we should be using sanity checks at each stage to verify that assumptions made in the code are actually true.

---

## General notes

- what are .bin files?
- Encryption is a two-way function where information is scrambled in such a way that it can be unscrambled later.
- "Hashing, one-way function where data is mapped to a fixed-length value. Hashing is primarily used for authentication. With a properly designed algorithm, there is no way to reverse the hashing process to reveal the original password."  So if there's a lookup dict that maps original sids to anons, is it really hashed?
- Salting is an additional step during hashing, typically seen in association to hashed passwords, that adds an additional value to the end of the password that changes the hash value produced. This adds a layer of security to the hashing process, specifically against brute force attacks. A brute force attack is where a computer or botnet attempt every possible combination of letters and numbers and characters until the password is found.  They can also attempt to hash every possible combination of letters and numbers and characters (companies use well known hashing functions?) until your pw is found, don't even have to know the actual password.  Adding salt creates unique pw's and therefore unique hashes so if a hacker finds one, he doesn't find another.    
