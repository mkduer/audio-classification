# audio classification
A short, fun project during a data science meetup. A good friend invited me to this meetup after attending the first session of four. The goal was to discern audio samples of digits generated by individuals in the meetup with various noise levels as well as data provided by the meetup organizers. 



Different groups and individuals came up with solutions to solve this problem using machine learning. Building off of our group's discussions, we decided turning the audio into images (specifically spectrograms) would make the learning much easier. 



I decided to take what I had learned from a Deep Learning class and create a convolutional neural network and pass the data through to see if it could classify the audio-turned-spectogram data. Four different data sets were used, but the most successful data was created by another group member who had trimmed the data that fell below a certain threshold. By doing this trimming, excess noise or absent noise seemed to be removed and resulted in cleaner data. 



Other data reached an accuracy of about 32% at the highest with high levels of overfitting demonstrated by high training accuracy, low test accuracy and cost plot readings. The trimmed spectrograms started at a higher level of accuracy with training accuracy in the 90s and testing accuracy ranging between 30-40%. TWhile various hyperparameter tweaking was performed with dropout, varying batch sizes, augmenting images, and more, the most successful increases in test accuracy resulted from minor tweaks with the learning rate and batch sizes using the adam optimizer.



The optimal learning rate was **η=0.0006-0.0007** with a batch size of **128** and  **4 layers** (including input/output layers). The concluding accuracy was consistently between **58-60% test accuracy**. Due to my school starting, I did not have the time to devote to further testing and tweaking the CNN, but would be interested in similar projects down the line as a fun hobby project.



Other means of tweaking the accuracy would be getting a more powerful GPU and adding more layers with larger images. My computer was not able to handle such a load, but I suspect the accuracy would have increased with higher resolution data. In addition, more tweaking to the images through augmentation (through very minuscule tweaks) would have been interesting to explore. A lot of the credit for the success is in the data pre-processing by @ViraTsintsadze as her work made a noted difference in accuracy results even prior to hyperparemter tweaking.
