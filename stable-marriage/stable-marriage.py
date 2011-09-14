
def find_stable_marriages_gs(males, females, preferences):
    """
    Finds a solution to stable marrigaes between all given males and females
    using the Gale & Shapley algorithm.
    
    Arguments:
    males -- The names of the males as strings.
    females -- The names of the females as strings.
    preferences -- A mapping name -> pref where name is a name of a male or 
                   female and pref is a list of names in order of preference for
                   that person.
    
    The result is a set of pairs (m, f) where m belongs to males and f to 
    females.
    
    Both males and females arguments must be of equal length, and preferences
    must have keys for all males and females and for every entry name -> pref
    pref must contain all females if name is a male name or all males if name is 
    a female name.
    """
    
    couples = [] # The temporary couples made by the algorithm.
    proposal_count_by_male = {} # A map of male -> n where n is the number of 
                                # females male has porposed to
                                
    # Makes a copy of the males to prevent parameter modification.
    males = males[:] 
    
    while males:
        proposals = [] # Marriage proposals for this round.
        
        # Every male proposes to his most-prefered female to which he hasn't yet
        # proposed.
        for male in males:
            proposal_count_by_male.setdefault(male, 0)
            female = preferences[male][proposal_count_by_male[male]]
            couple = (male, female)
            proposals.add(couple)
            proposal_count_by_male[male] += 1
        
        # Every female decides to take each proposal or not.
        for male, female in proposals:
            
            # Find her old fiance.
            old_male = next((m for m, f in couples if f == female), None)
            
            if not old_male:
                # She didn't have any fiance, she will be happier with this one.
                couple = (male, female)
                couples.add(couple)
                males.remove(male) # He's no longer single.
            else:
                # She had a fiance, choose the better one.
                prefs = preferences[female]
                if prefs.index(male) > prefs.index(old_male):
                    # The new one is preferable.
                    couple = (male, female)
                    couples.add(couple)
                    males.remove(male) # He's no longer single...
                    males.add(old_male) # Now her old fiance is!
    return couples

# OO Style...
class Person(object):
    def __init__(self, name, preferences):
        self.name = name
        self._preferences = preferences
        self._engagement = None
        print("Person", name, preferences)
        
    def is_engaged(self):
        return bool(self._engagement)

    def disengage(self):
        if self._engagement: 
            self._engagement._engagement = None
            self._engagement = None
    
    def engage_to(self, other):
        self.disengage()
        other.disengage()
        self._engagement = other
        other._engagement = self

class Female(Person):
    def prefers(self, male):
        return self.get_preference(male) < self.get_preference(_engagement)

    def get_preference(self, male):
        return self._preferences.index(male)

class Male(Person):
    def __init__(self, name, preferences):
        super(Male, self).__init__(name, preferences)
        self.clear_proposals()
        
    def clear_proposals(self):
        self._proposal_count = 0
    
    def next_proposal(self):
        p = self._preferences[_proposal_count]
        _proposal_count = 1
        return p

def stable_matching(males, females):
    # Set eveeryone to "free".
    for m in males:
        m.disengage()
        m.clear_proposals()
    
    def get_free_male():
        return next((m for m in males if not m.is_engaged()), None)
    
    while True:
        male = get_free_male()
        if not male:
            break
        female = male.next_proposal()
        if not female.is_engaged() or female.prefers(male):
            female.engage_to(male)

