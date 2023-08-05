#/bin/bash
# Get HTML:
wget http://blog.ig-conseils.com/plan-comptable-general/ -O PC_raw.html
#Keep plan comptable rows:
cat PC_raw.html | grep -E '.*[0-9][0-9]*\. *|CLASSE' | grep -E 'h1|h2|h3|strong|^[0-9]' > PC2.txt
#Clean up tags:
cat PC2.txt | sed -e 's/.*>\(CLASSE[^<]*\)<.*/\1/' -e 's/<h.>\([0-9]*.*\)<\/h.>/\1/' -e 's/<p>//' -e 's/<\/p>//' -e 's/<strong>//' -e 's/<\/strong>//'  -e 's/<br \/>//' -e 's/<h3>//'> PC3.txt
#Map accent and ampersand:
cat PC3.txt | sed -e "s/&#8217;/\'/g" -e "s/&#8211;/\&/g" -e "s+&rsquo;+'+g"> PC4.txt
#Remove useless info:
cat PC4.txt | sed -e 's/^CLASSE //' -e 's/ :/./' -e 's/\([0-9]*\)\. *\(.*\)/\1:\2/' -e 's/\.$//'> plan_comptable.txt
rm -f PC_raw.html PC2.txt PC3.txt PC4.txt
echo "Plan comptable generated: plan_comptable.txt"
