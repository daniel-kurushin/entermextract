from nltk.tokenize import WordPunctTokenizer as WPT
from nltk.corpus import stopwords as SW
from nltk.corpus import brown

stopwords = set(SW.words('english'))

wpt = WPT()

a_text = '''An absolutely convergent series, as follows from the above, is proved. In
general, the sum of the series strengthens the integral over the surface, from
which the equality to be proved follows. The counterexample attracts the
empirical Mobius leaf, thus the idiot's dream came true - the statement is
fully proved. A closed set synchronizes the Fourier integral, and any other
constant can be used instead of 13. A subset justifies a convergent series.
Until recently, it was assumed that the largest and smallest values of a
function are monotonic.

The primitive function synchronizes the curvilinear integral. The rational
number unwinds the Cauchy convergence criterion. The partial differential
equation is, of course, necessary and sufficient. The complex number supports
the jump function. The convergent series restores the maximum that is known
even to schoolchildren.

Mathematical analysis obviously concentrates the Hamilton integral. A closed
set stabilizes an empirical absolutely convergent series. The postulate, in
the first approximation, concentrates the parallel method of successive
approximations.'''.lower()

r_text = '''Абсолютно сходящийся ряд, как следует из вышесказанного, доказан. В общем, сумма ряда усиливает интеграл по поверхности, откуда следует доказываемое равенство. Контрпример притягивает эмпирический лист Мёбиуса, таким образом сбылась мечта идиота - утверждение полностью доказано. Замкнутое множество синхронизирует интеграл Фурье, при этом, вместо 13 можно взять любую другую константу. Подмножество оправдывает сходящийся ряд. До недавнего времени считалось, что наибольшее и наименьшее значения функции монотонно.
Первообразная функция синхронизирует криволинейный интеграл. Рациональное число раскручивает критерий сходимости Коши. Уравнение в частных производных, конечно, необходимо и достаточно. Комплексное число поддерживает скачок функции. Сходящийся ряд восстанавливает максимум, что известно даже школьникам.
Математический анализ, очевидно, концентрирует интеграл Гамильтона. Замкнутое множество стабилизирует эмпирический абсолютно сходящийся ряд. Постулат, в первом приближении, концентрирует параллельный метод последовательных приближений.'''

class TermExtractor():
    
    def __init__(self):
        the_corpora = [ x for x in brown.words()[:100000] if x not in set(".,*+=-'\"/\!1234567890()[]") and x not in stopwords ]
        frequrencies = []

        for n in range(1,5):
            n_gramms = [ the_corpora[i:i+n] for i in range(len(the_corpora)) ]
            for n_gramm in n_gramms:
                frequrencies += [(tuple(n_gramm), n_gramms.count(n_gramm))]


        self.freq_dict = {}

        for n_gramm, f in frequrencies:
            k = " ".join(n_gramm)
            self.freq_dict.update({k: f})
    

    def __call__(self, a_text, strings=1, limit=None):
        tokens = [ x for x in wpt.tokenize(a_text) if x not in set(".,*+=-'\"/\!1234567890()[]") and x not in stopwords ]
        
        local_frequrencies = []
        for n in range(1,5):
            n_gramms = [ tokens[i:i+n] for i in range(len(tokens)) ]
            for n_gramm in n_gramms:
                local_frequrencies += [(tuple(n_gramm), n_gramms.count(n_gramm))]
                
        local_frequrencies = set(local_frequrencies)
        
        kw = []
        n = 0
        for n_gramm, f0 in local_frequrencies:
            k = " ".join(n_gramm)
            try:
                f1 = self.freq_dict[k]
                f = f0 * f1
                if f:
                    kw += [(k, f0)]
            except KeyError:
                if f0 > 2:
                    kw += [(k, f0)]
            n += 1
                    
        kw = sorted(kw, key=lambda x:x[1], reverse=1)
        if limit:
            kw = kw[0:limit]
        return kw
    
if __name__ == '__main__':
    te = TermExtractor()
    print([ x for x in te(a_text) if x[0].count(' ') > 0 ])
    
    print([ x for x in te(b_text) if x[0].count(' ') > 0 ])
    from rutermextract import TermExtractor as TE
    te = TE()
    print([ x for x in te(r_text,strings=1) if x.count(' ') > 0 ])
