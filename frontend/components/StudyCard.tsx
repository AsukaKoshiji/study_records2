type Props = {
  title: string;
  hours: number;
  content: string;
  date: string;
};

export default function StudyCard({
  title,
  hours,
  content,
  date,
}: Props) {
  return (
    <div>
      <h2>{title}</h2>

      <p>{hours}時間</p>

      <p>{content}</p>

      <p>{date}</p>
    </div>
  );
}